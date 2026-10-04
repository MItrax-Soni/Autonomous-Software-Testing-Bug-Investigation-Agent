from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.session import TestSession
from app.models.page import DiscoveredPage
from app.models.element import DiscoveredElement
from app.schemas.topology import DiscoveredPageResponse, DiscoveredElementResponse
from app.services.crawler import WebCrawlerService
from app.services.ssrf_validator import SSRFSecurityError

router = APIRouter(prefix="/sessions", tags=["Scanner & Crawler"])

@router.post("/{session_id}/scan")
async def start_scan(session_id: str, db: AsyncSession = Depends(get_db)):
    crawler = WebCrawlerService(db=db)
    try:
        result = await crawler.crawl_target(session_id=session_id)
        return result
    except SSRFSecurityError as ssrf_err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ssrf_err))
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Crawl failed: {str(e)}")

@router.get("/{session_id}/pages", response_model=List[DiscoveredPageResponse])
async def get_session_pages(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(DiscoveredPage).where(DiscoveredPage.session_id == session_id).order_by(DiscoveredPage.depth.asc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{session_id}/elements", response_model=List[DiscoveredElementResponse])
async def get_session_elements(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(DiscoveredElement)
        .join(DiscoveredPage, DiscoveredElement.page_id == DiscoveredPage.id)
        .where(DiscoveredPage.session_id == session_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
