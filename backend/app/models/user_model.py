"""
user_model.py — MongoDB document structure for a user.
"""
from datetime import datetime, timezone


def new_user_doc(username: str, email: str, hashed_password: str) -> dict:
    """Return a fresh user document ready for insert_one()."""
    return {
        "username":        username.strip().lower(),
        "email":           email.strip().lower(),
        "hashed_password": hashed_password,
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }
