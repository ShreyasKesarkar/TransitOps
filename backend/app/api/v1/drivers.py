"""
app/api/v1/drivers.py

CRUD routes for the `drivers` table, plus a lightweight status-only
endpoint that the Driver App view uses to flip availability
(AVAILABLE / ON_TRIP / OFF_DUTY / SUSPENDED) without sending a full
DriverUpdate payload.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, require_roles
from app.core.database import get_db
from app.core.enums import DriverStatus
from app.crud import driver as driver_crud
from app.crud.exceptions import DuplicateError, NotFoundError
from app.models.user import User
from app.schemas.driver import DriverCreate, DriverRead, DriverStatusUpdate, DriverUpdate

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.get("", response_model=list[DriverRead])
async def list_drivers(
    status_filter: DriverStatus | None = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await driver_crud.get_drivers(db, status=status_filter, skip=skip, limit=limit)


@router.get("/{driver_id}", response_model=DriverRead)
async def get_driver(
    driver_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await driver_crud.get_driver(db, driver_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "",
    response_model=DriverRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("Admin", "Fleet Manager"))],
)
async def create_driver(
    driver_in: DriverCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await driver_crud.create_driver(db, driver_in, created_by=current_user.user_id)
    except DuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch(
    "/{driver_id}",
    response_model=DriverRead,
    dependencies=[Depends(require_roles("Admin", "Fleet Manager"))],
)
async def update_driver(
    driver_id: int,
    driver_in: DriverUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await driver_crud.update_driver(
            db, driver_id, driver_in, updated_by=current_user.user_id
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch("/{driver_id}/status", response_model=DriverRead)
async def update_driver_status(
    driver_id: int,
    status_in: DriverStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Driver App view calls this to toggle their own availability.
    Admin/Fleet Manager can update any driver; a Driver-role user may
    only update their own profile.
    """
    try:
        driver = await driver_crud.get_driver(db, driver_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    is_self = driver.user_id == current_user.user_id
    if not is_self:
        # Re-check privileged roles for anyone acting on someone else's driver profile.
        from sqlalchemy import select

        from app.models.role import Role

        result = await db.execute(select(Role.role_name).where(Role.role_id == current_user.role_id))
        role_name = result.scalar_one_or_none()
        if role_name not in ("Admin", "Fleet Manager"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You may only update your own driver status",
            )

    driver_update = DriverUpdate(driver_status=status_in.driver_status)
    return await driver_crud.update_driver(
        db, driver_id, driver_update, updated_by=current_user.user_id
    )


@router.delete(
    "/{driver_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles("Admin", "Fleet Manager"))],
)
async def delete_driver(
    driver_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    try:
        await driver_crud.soft_delete_driver(db, driver_id, updated_by=current_user.user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc