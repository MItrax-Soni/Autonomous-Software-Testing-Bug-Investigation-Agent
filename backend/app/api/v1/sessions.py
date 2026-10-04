import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.database import get_db, AsyncSessionLocal
from app.models.session import TestSession
from app.schemas.session import SessionCreate, SessionResponse
from app.services.orchestrator import AutonomousPipelineOrchestrator

router = APIRouter(prefix="/sessions", tags=["Sessions & Orchestration"])

@router.get("", response_model=List[SessionResponse])
async def list_sessions(
    project_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    query = select(TestSession).order_by(TestSession.started_at.desc()).limit(limit)
    if project_id:
        query = query.where(TestSession.project_id == project_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(payload: SessionCreate, db: AsyncSession = Depends(get_db)):
    session = TestSession(
        project_id=payload.project_id,
        target_url=str(payload.target_url),
        max_depth=payload.max_depth,
        max_pages=payload.max_pages,
        status="DRAFT"
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestSession).where(TestSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Test session not found")
    return session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestSession).where(TestSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Test session not found")
    await db.delete(session)
    await db.commit()
    return None

@router.post("/{session_id}/orchestrate")
async def orchestrate_full_pipeline(session_id: str, db: AsyncSession = Depends(get_db)):
    """
    Triggers the autonomous testing pipeline from crawling through reporting.
    """
    orchestrator = AutonomousPipelineOrchestrator(db=db)
    try:
        result = await orchestrator.run_full_pipeline(session_id=session_id)
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=404, detail=str(val_err))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(exc)}")

@router.get("/{session_id}/stream")
async def stream_session_progress(session_id: str):
    """
    Server-Sent Events (SSE) endpoint broadcasting session state transitions.
    """
    async def event_generator():
        for _ in range(30):
            async with AsyncSessionLocal() as db:
                res = await db.execute(select(TestSession).where(TestSession.id == session_id))
                session = res.scalar_one_or_none()
                if not session:
                    yield f"data: {json.dumps({'error': 'Session not found'})}\n\n"
                    break

                payload = {
                    "id": session.id,
                    "status": session.status,
                    "total_tests": session.total_tests,
                    "passed_tests": session.passed_tests,
                    "failed_tests": session.failed_tests
                }
                yield f"data: {json.dumps(payload)}\n\n"

                if session.status in ("COMPLETED", "FAILED"):
                    break

            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
