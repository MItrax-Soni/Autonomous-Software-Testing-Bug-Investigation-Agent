from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import time

from app.config import settings
from app.database import init_db
from app.api.v1.router import api_v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    await init_db()
    yield

app = FastAPI(
    title="Autonomous Software Testing & Bug Investigation Agent API",
    description="Autonomous web crawler, AI test scenario generator, Playwright execution sandbox, and root-cause bug investigator.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for the frontend command center
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure artifacts directory exists and mount for direct evidence inspection
artifacts_path = Path(settings.ARTIFACTS_DIR)
artifacts_path.mkdir(parents=True, exist_ok=True)
app.mount("/artifacts", StaticFiles(directory=str(artifacts_path)), name="artifacts")

# Register unified v1 router
app.include_router(api_v1_router)

@app.get("/")
async def root():
    return {
        "service": "Autonomous Software Testing & Bug Investigation Agent",
        "status": "online",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": settings.ENVIRONMENT,
        "database_configured": bool(settings.DATABASE_URL),
        "gemini_configured": bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here"),
        "ssrf_protection": settings.SSRF_PROTECTION_ENABLED,
        "controlled_local_testing": settings.SSRF_ALLOW_CONTROLLED_LOCAL_APP
    }
