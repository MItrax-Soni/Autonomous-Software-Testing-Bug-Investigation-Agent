from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Workspace root is two levels up from backend/app
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = WORKSPACE_ROOT / ".env"

class Settings(BaseSettings):
    # AI Intelligence (Google Gemini)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Backend API Service
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Database Persistence
    DATABASE_URL: str = "sqlite+aiosqlite:///./test_agent.db"

    # Browser Automation (Playwright)
    PLAYWRIGHT_HEADLESS: bool = True
    PLAYWRIGHT_DEFAULT_TIMEOUT_MS: int = 30000
    PLAYWRIGHT_ACTION_TIMEOUT_MS: int = 5000
    BROWSER_VIEWPORT_WIDTH: int = 1280
    BROWSER_VIEWPORT_HEIGHT: int = 800

    # Security & SSRF Protection
    SSRF_PROTECTION_ENABLED: bool = True
    SSRF_ALLOW_CONTROLLED_LOCAL_APP: bool = True
    CONTROLLED_LOCAL_APP_PORT: int = 8088

    # Evidence & Artifacts
    ARTIFACTS_DIR: str = str(WORKSPACE_ROOT / "artifacts")

    # Frontend Application
    VITE_API_BASE_URL: str = "http://127.0.0.1:8000/api/v1"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH) if ENV_FILE_PATH.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
