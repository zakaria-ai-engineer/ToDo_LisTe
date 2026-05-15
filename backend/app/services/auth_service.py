"""
auth_service.py — User registration, login, and JWT issuance.
"""
from fastapi import HTTPException, status
from app.config.database import get_users_collection
from app.config.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token
from app.models.user_model import new_user_doc
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse
from app.utils.helpers import serialize_doc


def register_user(data: RegisterRequest) -> TokenResponse:
    users = get_users_collection()

    # Vérification atomique des doublons (username OU email) en une seule requête
    existing = users.find_one({
        "$or": [
            {"username": data.username.strip().lower()},
            {"email":    data.email.strip().lower()},
        ]
    })
    if existing:
        if existing.get("email") == data.email.strip().lower():
            raise HTTPException(status_code=409, detail="Cet email est déjà utilisé.")
        raise HTTPException(status_code=409, detail="Ce nom d'utilisateur est déjà pris.")

    doc    = new_user_doc(data.username, data.email, hash_password(data.password))
    result = users.insert_one(doc)
    created = users.find_one({"_id": result.inserted_id})

    token = create_access_token({"sub": created["username"], "id": str(created["_id"])})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        username=created["username"],
        email=created["email"],
    )


def login_user(data: LoginRequest) -> TokenResponse:
    users = get_users_collection()
    # Login by email (matches frontend form)
    user = users.find_one({"email": data.email.lower()})

    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
        )

    token = create_access_token({"sub": user["username"], "id": str(user["_id"])})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        username=user["username"],
        email=user["email"],
    )
