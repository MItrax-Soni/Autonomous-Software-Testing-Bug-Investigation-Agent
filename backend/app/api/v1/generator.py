from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.session import TestSession
from app.models.page import DiscoveredPage
from app.models.element import DiscoveredElement
from app.models.scenario import TestScenario
from app.schemas.scenario import ScenarioResponse, ScenarioUpdate
from app.services.gemini_client import gemini_service

router = APIRouter(prefix="/sessions", tags=["AI Test Planning"])

@router.post("/{session_id}/generate-scenarios")
async def generate_scenarios(session_id: str, db: AsyncSession = Depends(get_db)):
    # 1. Fetch Session
    session_res = await db.execute(select(TestSession).where(TestSession.id == session_id))
    session = session_res.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Test session not found")

    # 2. Fetch Discovered Pages & Elements
    pages_res = await db.execute(select(DiscoveredPage).where(DiscoveredPage.session_id == session_id))
    pages = pages_res.scalars().all()

    elements_res = await db.execute(
        select(DiscoveredElement)
        .join(DiscoveredPage, DiscoveredElement.page_id == DiscoveredPage.id)
        .where(DiscoveredPage.session_id == session_id)
    )
    elements = elements_res.scalars().all()

    pages_dict = [{"url": p.url, "title": p.title} for p in pages]
    elements_dict = [
        {
            "tag_name": el.tag_name,
            "element_type": el.element_type,
            "selector": el.selector,
            "semantic_label": el.semantic_label
        }
        for el in elements
    ]

    # 3. Generate Scenarios via Gemini or Heuristic fallback
    generated_raw = await gemini_service.generate_test_scenarios(
        target_url=session.target_url,
        pages=pages_dict,
        elements=elements_dict
    )

    # 4. Clear any previously generated scenarios for this session
    old_scenarios = await db.execute(select(TestScenario).where(TestScenario.session_id == session_id))
    for old_s in old_scenarios.scalars().all():
        await db.delete(old_s)

    # 5. Persist new scenarios
    persisted_scenarios = []
    for idx, sc in enumerate(generated_raw):
        db_scenario = TestScenario(
            session_id=session.id,
            title=sc.get("title", f"Test Scenario #{idx + 1}"),
            description=sc.get("description", "Autonomous test scenario"),
            category=sc.get("category", "POSITIVE"),
            target_page_url=sc.get("target_page_url", session.target_url),
            steps_json=sc.get("steps_json", []),
            expected_result=sc.get("expected_result", "Expected successful state outcome."),
            is_approved=sc.get("is_approved", True),
            order_index=sc.get("order_index", idx + 1)
        )
        db.add(db_scenario)
        persisted_scenarios.append(db_scenario)

    session.status = "PLANNED"
    session.total_tests = len(persisted_scenarios)
    await db.commit()

    return {
        "status": "PLANNED",
        "count": len(persisted_scenarios),
        "scenarios": [
            {
                "id": s.id,
                "title": s.title,
                "category": s.category,
                "steps": s.steps_json,
                "is_approved": s.is_approved
            }
            for s in persisted_scenarios
        ]
    }

@router.get("/{session_id}/scenarios", response_model=List[ScenarioResponse])
async def get_session_scenarios(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(TestScenario).where(TestScenario.session_id == session_id).order_by(TestScenario.order_index.asc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.put("/{session_id}/scenarios/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    session_id: str,
    scenario_id: str,
    payload: ScenarioUpdate,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(TestScenario).where(
        TestScenario.id == scenario_id,
        TestScenario.session_id == session_id
    )
    result = await db.execute(stmt)
    scenario = result.scalar_one_or_none()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    if payload.is_approved is not None:
        scenario.is_approved = payload.is_approved
    if payload.order_index is not None:
        scenario.order_index = payload.order_index
    if payload.title is not None:
        scenario.title = payload.title
    if payload.steps_json is not None:
        scenario.steps_json = [s.model_dump() for s in payload.steps_json]

    await db.commit()
    await db.refresh(scenario)
    return scenario
