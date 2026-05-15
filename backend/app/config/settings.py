"""
settings.py — Centralized application configuration.
Forces .env loading via dotenv with an absolute path BEFORE Pydantic reads anything.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# ── Résolution du chemin absolu vers backend/.env ─────────────────────────────
# Ce fichier est à : backend/app/config/settings.py
#   .parent   → backend/app/config/
#   .parent   → backend/app/
#   .parent   → backend/          ← BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# Force le chargement avec override=True (écrase tout env déjà en mémoire)
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Erreur fatale visible dans la console serveur si la clé manque encore
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError(
        f"CRITICAL ERROR: GEMINI_API_KEY est introuvable. "
        f"Chemin cherché : {ENV_PATH} — "
        f"Fichier existe : {ENV_PATH.exists()}"
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    APP_NAME: str = "TaskBot AI"
    APP_VERSION: str = "3.0.0"
    DEBUG: bool = False

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017/"
    DB_NAME: str = "taskbot_db"

    # Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    LLM_TEMPERATURE: float = 0.2

    # JWT / Security
    JWT_SECRET_KEY: str = "change-me-use-openssl-rand-hex-32"
    SECRET_KEY: str = "change-me-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours


settings = Settings()
