from fastapi import APIRouter
from app.api.v1.projects import router as projects_router
from app.api.v1.sessions import router as sessions_router
from app.api.v1.scanner import router as scanner_router
from app.api.v1.generator import router as generator_router
from app.api.v1.execution import router as execution_router
from app.api.v1.investigation import router as investigation_router
from app.api.v1.reports import router as reports_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(projects_router)
api_v1_router.include_router(sessions_router)
api_v1_router.include_router(scanner_router)
api_v1_router.include_router(generator_router)
api_v1_router.include_router(execution_router)
api_v1_router.include_router(investigation_router)
api_v1_router.include_router(reports_router)
