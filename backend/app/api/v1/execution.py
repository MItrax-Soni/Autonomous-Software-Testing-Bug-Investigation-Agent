from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.database import get_db
from app.models.execution import TestExecution, ExecutionStep
from app.models.scenario import TestScenario
from app.schemas.execution import TestExecutionResponse
from app.services.test_runner import DeterministicTestRunner

router = APIRouter(prefix="/sessions", tags=["Test Execution"])

@router.post("/{session_id}/execute")
async def execute_tests(session_id: str, db: AsyncSession = Depends(get_db)):
    runner = DeterministicTestRunner(db=db)
    try:
        result = await runner.execute_approved_scenarios(session_id=session_id)
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=404, detail=str(val_err))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(exc)}")

@router.get("/{session_id}/executions", response_model=List[TestExecutionResponse])
async def get_session_executions(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(TestExecution)
        .options(
            selectinload(TestExecution.steps),
            selectinload(TestExecution.scenario)
        )
        .where(TestExecution.session_id == session_id)
        .order_by(TestExecution.executed_at.asc())
    )
    result = await db.execute(stmt)
    executions = result.scalars().all()

    # Populate scenario_title for response
    response_list = []
    for ex in executions:
        ex_resp = TestExecutionResponse(
            id=ex.id,
            scenario_id=ex.scenario_id,
            session_id=ex.session_id,
            scenario_title=ex.scenario.title if ex.scenario else "Test Scenario",
            status=ex.status,
            duration_ms=ex.duration_ms,
            error_message=ex.error_message,
            error_step_index=ex.error_step_index,
            executed_at=ex.executed_at,
            steps=[
                {
                    "id": st.id,
                    "step_index": st.step_index,
                    "action": st.action,
                    "selector": st.selector,
                    "value": st.value,
                    "status": st.status,
                    "duration_ms": st.duration_ms,
                    "error_log": st.error_log,
                    "screenshot_path": st.screenshot_path
                }
                for st in ex.steps
            ]
        )
        response_list.append(ex_resp)

    return response_list
