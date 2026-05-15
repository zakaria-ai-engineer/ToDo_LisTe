"""
TaskBot AI — Backend (FastAPI + PyMongo + Gemini 1.5 Flash + JWT Auth)
=======================================================================
Architecture complète avec :
  - Authentification JWT (register / login / get_current_user)
  - Validation stricte Pydantic
  - Gemini AI avec JSON forcé
  - MongoDB (collection tasks liée à l'user_id)
  - CORS pour le frontend React
"""

import os
import json
import re
from datetime import datetime, timezone, timedelta
from typing import Optional, Literal

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr, field_validator
from pymongo import MongoClient, DESCENDING
from bson import ObjectId
import google.generativeai as genai
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────────────
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
MONGODB_URL     = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
JWT_SECRET_KEY  = os.getenv("JWT_SECRET_KEY", "changeme_secret")
ALGORITHM       = os.getenv("ALGORITHM", "HS256")
TOKEN_EXPIRE_H  = 24  # hours

# Gemini
genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "Tu es le cerveau d'un système de To-Do List. "
    "Tu dois UNIQUEMENT retourner un JSON strict sans aucun texte supplémentaire.\n"
    "FORMAT OBLIGATOIRE :\n"
    '{"action": "add_task|delete_task|show_tasks", '
    '"task": "nom de la tâche ou null", '
    '"priority": "high|medium|low", '
    '"bot_reply": "Message court en Darija ou Français"}'
)

gemini_model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT,
    generation_config={"response_mime_type": "application/json", "temperature": 0.2},
)

# ──────────────────────────────────────────────────────────────────────────────
# MongoDB
# ──────────────────────────────────────────────────────────────────────────────
mongo_client = MongoClient(MONGODB_URL)
db           = mongo_client["taskbot_db"]
tasks_col    = db["tasks"]
users_col    = db["users"]

# Index unique sur l'email pour les users
users_col.create_index("email", unique=True)
users_col.create_index("username", unique=True)

# ──────────────────────────────────────────────────────────────────────────────
# Password hashing
# ──────────────────────────────────────────────────────────────────────────────
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

# ──────────────────────────────────────────────────────────────────────────────
# JWT Helpers
# ──────────────────────────────────────────────────────────────────────────────
def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_H)
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise ValueError
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré. Reconnectez-vous.")
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide.")
    user = users_col.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable.")
    return user

# ──────────────────────────────────────────────────────────────────────────────
# Pydantic Schemas — Validation stricte
# ──────────────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    """Schéma d'inscription : valide l'email, le nom d'utilisateur et le mot de passe."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=6, max_length=128)

    @field_validator("username")
    @classmethod
    def username_no_spaces(cls, v: str) -> str:
        if " " in v:
            raise ValueError("Le nom d'utilisateur ne doit pas contenir d'espaces.")
        return v.strip()


class UserLogin(BaseModel):
    """Schéma de connexion : email + mot de passe."""
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class ChatMessage(BaseModel):
    """Message envoyé par l'utilisateur au chatbot."""
    message: str = Field(..., min_length=1, max_length=1000, strip_whitespace=True)


class TaskUpdateRequest(BaseModel):
    """Mise à jour partielle d'une tâche via l'UI."""
    task:     Optional[str]                              = Field(None, min_length=1, max_length=500)
    priority: Optional[Literal["low", "medium", "high"]] = None
    done:     Optional[bool]                             = None

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
def serialize_task(task: dict) -> dict:
    task["_id"] = str(task["_id"])
    return task

def extract_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    raise ValueError(f"JSON invalide: {text[:300]}")

# ──────────────────────────────────────────────────────────────────────────────
# FastAPI Application
# ──────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="TaskBot AI",
    description="Intelligent To-Do List — Gemini 1.5 Flash + FastAPI + MongoDB",
    version="3.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "TaskBot AI v3.1", "model": "gemini-1.5-flash"}

# ──────────────────────────────────────────────────────────────────────────────
# AUTH ROUTES
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/register", tags=["Auth"], status_code=status.HTTP_201_CREATED)
def register(body: UserCreate):
    """Inscription d'un nouvel utilisateur avec mot de passe hashé (bcrypt)."""
    if users_col.find_one({"email": body.email}):
        raise HTTPException(status_code=409, detail="Cet email est déjà utilisé.")
    if users_col.find_one({"username": body.username}):
        raise HTTPException(status_code=409, detail="Ce nom d'utilisateur est déjà pris.")

    result = users_col.insert_one({
        "email":      body.email,
        "username":   body.username,
        "password":   hash_password(body.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    token = create_access_token({"sub": str(result.inserted_id)})
    return {"access_token": token, "token_type": "bearer", "username": body.username}


@app.post("/login", tags=["Auth"])
def login(body: UserLogin):
    """Connexion : vérifie les identifiants et retourne un JWT."""
    user = users_col.find_one({"email": body.email})
    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer", "username": user["username"]}


@app.get("/me", tags=["Auth"])
def me(current_user: dict = Depends(get_current_user)):
    """Retourne l'utilisateur connecté (nécessite un token JWT valide)."""
    return {"id": str(current_user["_id"]), "username": current_user["username"], "email": current_user["email"]}

# ──────────────────────────────────────────────────────────────────────────────
# CHAT ROUTE (Protégée JWT)
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/chat", tags=["AI"])
async def chat(req: ChatMessage, current_user: dict = Depends(get_current_user)):
    """
    Route protégée JWT.
    - Envoie le message à Gemini 1.5 Flash.
    - Parse la réponse JSON stricte.
    - Exécute l'action dans MongoDB (tasks liées à l'user_id).
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "ta_cle_gemini_ici":
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY manquante dans .env")

    user_id = str(current_user["_id"])

    # ── Appel Gemini ──────────────────────────────────────────────────────────
    try:
        response = gemini_model.generate_content(req.message)
        raw_output = response.text
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur API Gemini: {e}")

    # ── Parse JSON ────────────────────────────────────────────────────────────
    try:
        parsed = extract_json(raw_output)
    except (ValueError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=422, detail=f"Réponse Gemini invalide: {e}")

    action    = parsed.get("action")
    task_name = parsed.get("task")
    priority  = parsed.get("priority") if parsed.get("priority") in ("low", "medium", "high") else "medium"
    bot_reply = parsed.get("bot_reply", "✅ Action traitée!")

    # ── Exécution MongoDB ─────────────────────────────────────────────────────
    try:
        if action == "add_task":
            if not task_name or not task_name.strip():
                raise HTTPException(status_code=400, detail="Nom de tâche requis.")
            tasks_col.insert_one({
                "user_id":    user_id,
                "task":       task_name.strip(),
                "priority":   priority,
                "done":       False,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
        elif action == "delete_task":
            if not task_name or not task_name.strip():
                raise HTTPException(status_code=400, detail="Nom de tâche requis.")
            tasks_col.delete_many({
                "user_id": user_id,
                "task": {"$regex": re.escape(task_name.strip()), "$options": "i"},
            })
        elif action == "show_tasks":
            pass  # Le frontend appelle GET /tasks
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur MongoDB: {e}")

    return {"bot_reply": bot_reply, "action": action}

# ──────────────────────────────────────────────────────────────────────────────
# TASKS ROUTES (Protégées JWT)
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/tasks", tags=["Tasks"])
def get_tasks(current_user: dict = Depends(get_current_user)):
    """Retourne uniquement les tâches de l'utilisateur connecté."""
    user_id = str(current_user["_id"])
    try:
        tasks = list(tasks_col.find({"user_id": user_id}).sort("created_at", DESCENDING))
        return [serialize_task(t) for t in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur MongoDB: {e}")


@app.put("/tasks/{task_id}", tags=["Tasks"])
def update_task(
    task_id: str,
    body: TaskUpdateRequest,
    current_user: dict = Depends(get_current_user),
):
    """Mise à jour partielle d'une tâche par son ID (liée à l'utilisateur)."""
    user_id = str(current_user["_id"])
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de tâche invalide.")

    update_fields = {k: v for k, v in body.model_dump().items() if v is not None}
    if not update_fields:
        return {"status": "no_update"}

    try:
        result = tasks_col.update_one(
            {"_id": oid, "user_id": user_id},
            {"$set": update_fields},
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Tâche introuvable.")
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur MongoDB: {e}")


@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task_by_id(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Supprime une tâche par son ID (liée à l'utilisateur)."""
    user_id = str(current_user["_id"])
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de tâche invalide.")
    try:
        result = tasks_col.delete_one({"_id": oid, "user_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Tâche introuvable.")
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur MongoDB: {e}")
