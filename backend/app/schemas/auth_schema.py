"""
auth_schema.py — Pydantic schemas for authentication.
"""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email:    EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=6, max_length=100)


class LoginRequest(BaseModel):
    """Frontend sends { email, password } — NOT username."""
    email:    EmailStr
    password: str = Field(..., min_length=1, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    username:     str
    email:        str


class UserResponse(BaseModel):
    id:         str
    username:   str
    email:      str
    created_at: str
