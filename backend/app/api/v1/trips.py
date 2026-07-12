"""
app/api/v1/trips.py

CRUD routes for the `trips` table. Trip creation/reassignment is an
Admin / Fleet Manager action (dispatching). The lightweight status-only
endpoint is what the Driver App view calls to move a trip through
PLANNED -> IN_PROGRESS -> COMPLETED, and is restricted to the driver
actually assigned to that trip (or Admin / Fleet Manager as an override).

Note: trips have no soft-delete columns in the SQL schema, so DELETE
here is a genuine hard delete (see app/crud/trip.py docstring).
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, require_roles
from app.core.database import get_db
from app.core.enums import TripStatus
from app.crud import driver as driver_crud
from app.crud import trip as trip_crud
from app.crud.exceptions import DuplicateError, NotFoundError
from app.models.role import Role
from app.models.user import User
from app.schemas.trip import TripCreate, TripRead, TripReadDetailed, TripStatusUpdate, TripUpdate

router = APIRouter(prefix="/trips", tags=["Trips"])


async def _get_role_name(db: AsyncSession, role_id: int) -> str | None:
    result = await db.execute(select(Role.role_name).where(Role.role_id == role_id))
    return result.scalar_one_or_none()


@router.get("", response_model=list[TripReadDetailed])
async def list_trips(
    organization_id: int | None = Query(None),
    status_filter: TripStatus | None = Query(None, alias="status"),
    driver_id: int | None = Query(None),
    vehicle_id: int | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await trip_crud.get_trips(
        db,
        organization_id=organization_id,
        status=status_filter,
        driver_id=driver_id,
        vehicle_id=vehicle_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{trip_id}", response_model=TripReadDetailed)
async def get_trip(
    trip_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await trip_crud.get_trip(db, trip_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "",
    response_model=TripRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("Admin", "Fleet Manager"))],
)
async def create_trip(
    trip_in: TripCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await trip_crud.create_trip(db, trip_in, created_by=current_user.user_id)
    except DuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch(
    "/{trip_id}",
    response_model=TripRead,
    dependencies=[Depends(require_roles("Admin", "Fleet Manager"))],
)
async def update_trip(
    trip_id: int,
    trip_in: TripUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await trip_crud.update_trip(db, trip_id, trip_in, updated_by=current_user.user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{trip_id}/status", response_model=TripRead)
async def update_trip_status(
    trip_id: int,
    status_in: TripStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Driver App view calls this to move a trip through its lifecycle.
    Allowed for the driver assigned to the trip, or Admin / Fleet Manager
    as a dispatcher override.
    """
    try:
        trip = await trip_crud.get_trip(db, trip_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    role_name = await _get_role_name(db, current_user.role_id)

    is_assigned_driver = False
    if role_name == "Driver":
        driver_profile = await driver_crud.get_driver_by_user_id(db, current_user.user_id)
        is_assigned_driver = driver_profile is not None and driver_profile.driver_id == trip.driver_id

    if role_name not in ("Admin", "Fleet Manager") and not is_assigned_driver:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You may only update the status of trips assigned to you",
        )

    return await trip_crud.update_trip_status(
        db, trip_id, status_in.trip_status, updated_by=current_user.user_id
    )


@router.delete(
    "/{trip_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles("Admin"))],
)
async def delete_trip(
    trip_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    try:
        await trip_crud.delete_trip(db, trip_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc