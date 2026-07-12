"""
app/api/v1/vehicles.py

CRUD routes for the `vehicles` table. Any authenticated user can read
(dispatchers/drivers need this for trip assignment + live map); writes
are restricted to Admin / Fleet Manager.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, require_roles
from app.core.database import get_db
from app.core.enums import VehicleStatus
from app.crud import vehicle as vehicle_crud
from app.crud.exceptions import DuplicateError, NotFoundError
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.get("", response_model=list[VehicleRead])
async def list_vehicles(
    organization_id: int | None = Query(None),
    status_filter: VehicleStatus | None = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await vehicle_crud.get_vehicles(
        db, organization_id=organization_id, status=status_filter, skip=skip, limit=limit
    )


@router.get("/{vehicle_id}", response_model=VehicleRead)
async def get_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await vehicle_crud.get_vehicle(db, vehicle_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "",
    response_model=VehicleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("Admin", "Fleet Manager"))],
)
async def create_vehicle(
    vehicle_in: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await vehicle_crud.create_vehicle(db, vehicle_in, created_by=current_user.user_id)
    except DuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch(
    "/{vehicle_id}",
    response_model=VehicleRead,
    dependencies=[Depends(require_roles("Admin", "Fleet Manager"))],
)
async def update_vehicle(
    vehicle_id: int,
    vehicle_in: VehicleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await vehicle_crud.update_vehicle(
            db, vehicle_id, vehicle_in, updated_by=current_user.user_id
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles("Admin", "Fleet Manager"))],
)
async def delete_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    try:
        await vehicle_crud.soft_delete_vehicle(db, vehicle_id, updated_by=current_user.user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc