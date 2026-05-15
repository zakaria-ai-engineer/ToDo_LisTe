"""
auth_routes.py — /register, /login, /me endpoints.
Routes match the frontend api.js calls exactly (no /auth prefix).
"""
from fastapi import APIRouter, Depends
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import register_user, login_user
from app.middleware.auth_middleware import get_current_user

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: RegisterRequest):
    """Register a new user and return a JWT token immediately."""
    return register_user(data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    """Authenticate with email + password and receive a JWT token."""
    return login_user(data)


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    """Return the currently authenticated user info."""
    return {"user_id": user["user_id"], "username": user["username"]}
