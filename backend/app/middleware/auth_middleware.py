"""
auth_middleware.py — FastAPI dependency to extract and validate JWT from request.
Usage: Depends(get_current_user) on any protected route.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.jwt_handler import decode_access_token

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """
    Dependency that validates the Bearer JWT and returns the decoded payload.
    Raises HTTP 401 if token is missing, invalid, or expired.
    """
    token   = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("id")
    username = payload.get("sub")

    if not user_id or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return {"user_id": user_id, "username": username}
