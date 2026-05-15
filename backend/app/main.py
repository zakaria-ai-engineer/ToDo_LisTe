"""
main.py — FastAPI application entry point.
Registers all routers, CORS middleware, and MongoDB lifecycle hooks.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.config.database import Database
from app.routes import auth_routes, task_routes, chat_routes

app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent To-Do chatbot powered by Gemini 2.5 Flash + FastAPI + MongoDB",
    version=settings.APP_VERSION,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── MongoDB lifecycle ─────────────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    Database.connect()


@app.on_event("shutdown")
def shutdown():
    Database.disconnect()

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_routes.router)
app.include_router(task_routes.router)
app.include_router(chat_routes.router)


@app.get("/", tags=["Health"])
def health():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "model": settings.GEMINI_MODEL,
    }
