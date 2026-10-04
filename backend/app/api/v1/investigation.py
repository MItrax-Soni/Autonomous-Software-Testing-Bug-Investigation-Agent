from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.database import get_db
from app.models.bug import Bug
from app.models.evidence import EvidenceItem
from app.schemas.bug import BugResponse
from app.services.bug_investigator import BugInvestigationService

router = APIRouter(tags=["Bug Investigation"])

@router.get("/sessions/{session_id}/bugs", response_model=List[BugResponse])
async def get_session_bugs(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Bug)
        .options(selectinload(Bug.evidence_items))
        .where(Bug.session_id == session_id)
        .order_by(Bug.created_at.desc())
    )
    result = await db.execute(stmt)
    bugs = result.scalars().all()

    response_list = []
    for bug in bugs:
        screenshot_item = next((e for e in bug.evidence_items if e.evidence_type == "SCREENSHOT"), None)
        response_list.append(
            BugResponse(
                id=bug.id,
                execution_id=bug.execution_id,
                session_id=bug.session_id,
                title=bug.title,
                category=bug.category,
                severity=bug.severity,
                verified_evidence_json=bug.verified_evidence_json,
                ai_hypothesis_json=bug.ai_hypothesis_json,
                remediation_advice=bug.remediation_advice,
                screenshot_url=screenshot_item.file_path if screenshot_item else None,
                created_at=bug.created_at
            )
        )
    return response_list

@router.get("/bugs/{bug_id}", response_model=BugResponse)
async def get_bug_detail(bug_id: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Bug)
        .options(selectinload(Bug.evidence_items))
        .where(Bug.id == bug_id)
    )
    result = await db.execute(stmt)
    bug = result.scalar_one_or_none()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug finding not found")

    screenshot_item = next((e for e in bug.evidence_items if e.evidence_type == "SCREENSHOT"), None)
    return BugResponse(
        id=bug.id,
        execution_id=bug.execution_id,
        session_id=bug.session_id,
        title=bug.title,
        category=bug.category,
        severity=bug.severity,
        verified_evidence_json=bug.verified_evidence_json,
        ai_hypothesis_json=bug.ai_hypothesis_json,
        remediation_advice=bug.remediation_advice,
        screenshot_url=screenshot_item.file_path if screenshot_item else None,
        created_at=bug.created_at
    )

@router.post("/executions/{execution_id}/investigate", response_model=BugResponse)
async def trigger_investigation(execution_id: str, db: AsyncSession = Depends(get_db)):
    investigator = BugInvestigationService(db=db)
    bug = await investigator.investigate_failed_execution(execution_id=execution_id)
    if not bug:
        raise HTTPException(status_code=400, detail="Execution is not in FAILED state or not found")

    return BugResponse(
        id=bug.id,
        execution_id=bug.execution_id,
        session_id=bug.session_id,
        title=bug.title,
        category=bug.category,
        severity=bug.severity,
        verified_evidence_json=bug.verified_evidence_json,
        ai_hypothesis_json=bug.ai_hypothesis_json,
        remediation_advice=bug.remediation_advice,
        created_at=bug.created_at
    )
