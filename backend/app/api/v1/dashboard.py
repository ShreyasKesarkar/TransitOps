"""
app/api/v1/dashboard.py

Read-only aggregation endpoint for the Admin Dashboard's metric cards
and charts. Open to any authenticated user for now; tighten to
Admin/Fleet Manager only if the dashboard shouldn't be driver-visible.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import get_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def dashboard_summary(
    organization_id: int | None = Query(
        None, description="Scope metrics to one organization; omit for platform-wide."
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DashboardSummary:
    return await get_dashboard_summary(db, organization_id=organization_id)