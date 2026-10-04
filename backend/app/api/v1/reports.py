from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.report import Report
from app.schemas.report import ReportResponse
from app.services.report_generator import ReportGeneratorService

router = APIRouter(prefix="/sessions", tags=["Reports"])

@router.post("/{session_id}/report", response_model=ReportResponse)
async def generate_report(session_id: str, db: AsyncSession = Depends(get_db)):
    service = ReportGeneratorService(db=db)
    try:
        report = await service.generate_session_report(session_id=session_id)
        return report
    except ValueError as val_err:
        raise HTTPException(status_code=404, detail=str(val_err))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Report generation error: {str(exc)}")

@router.get("/{session_id}/report", response_model=ReportResponse)
async def get_report(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Report).where(Report.session_id == session_id)
    res = await db.execute(stmt)
    report = res.scalar_one_or_none()
    if not report:
        # Synthesize on demand if not existing yet
        service = ReportGeneratorService(db=db)
        try:
            report = await service.generate_session_report(session_id=session_id)
        except Exception:
            raise HTTPException(status_code=404, detail="Report not available for this session")

    return report

@router.get("/{session_id}/report/download", response_class=PlainTextResponse)
async def download_report_markdown(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Report).where(Report.session_id == session_id)
    res = await db.execute(stmt)
    report = res.scalar_one_or_none()
    if not report:
        service = ReportGeneratorService(db=db)
        report = await service.generate_session_report(session_id=session_id)

    return PlainTextResponse(
        content=report.summary_markdown,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=report_{session_id}.md"}
    )
