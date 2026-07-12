"""
app/crud/vehicle.py

Data-access layer for the `vehicles` table.
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.enums import VehicleStatus
from app.crud.exceptions import DuplicateError, NotFoundError
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


async def get_vehicle(db: AsyncSession, vehicle_id: int) -> Vehicle:
    result = await db.execute(
        select(Vehicle)
        .options(selectinload(Vehicle.vehicle_type))
        .where(Vehicle.vehicle_id == vehicle_id, Vehicle.is_deleted.is_(False))
    )
    vehicle = result.scalar_one_or_none()
    if vehicle is None:
        raise NotFoundError(f"Vehicle {vehicle_id} not found")
    return vehicle


async def get_vehicle_by_registration(db: AsyncSession, registration_number: str) -> Vehicle | None:
    result = await db.execute(
        select(Vehicle).where(
            Vehicle.registration_number == registration_number, Vehicle.is_deleted.is_(False)
        )
    )
    return result.scalar_one_or_none()


async def get_vehicles(
    db: AsyncSession,
    organization_id: int | None = None,
    status: VehicleStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Vehicle]:
    stmt = (
        select(Vehicle)
        .options(selectinload(Vehicle.vehicle_type))
        .where(Vehicle.is_deleted.is_(False))
    )
    if organization_id is not None:
        stmt = stmt.where(Vehicle.organization_id == organization_id)
    if status is not None:
        stmt = stmt.where(Vehicle.vehicle_status == status)
    stmt = stmt.offset(skip).limit(limit).order_by(Vehicle.vehicle_id)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_vehicle(
    db: AsyncSession, vehicle_in: VehicleCreate, created_by: int | None = None
) -> Vehicle:
    existing = await get_vehicle_by_registration(db, vehicle_in.registration_number)
    if existing is not None:
        raise DuplicateError(
            f"Registration number '{vehicle_in.registration_number}' is already in use"
        )

    vehicle = Vehicle(
        organization_id=vehicle_in.organization_id,
        vehicle_type_id=vehicle_in.vehicle_type_id,
        vehicle_code=vehicle_in.vehicle_code,
        registration_number=vehicle_in.registration_number,
        manufacturer=vehicle_in.manufacturer,
        model=vehicle_in.model,
        manufacturing_year=vehicle_in.manufacturing_year,
        maximum_load_capacity=vehicle_in.maximum_load_capacity,
        odometer=vehicle_in.odometer,
        acquisition_cost=vehicle_in.acquisition_cost,
        created_by=created_by,
    )
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


async def update_vehicle(
    db: AsyncSession, vehicle_id: int, vehicle_in: VehicleUpdate, updated_by: int | None = None
) -> Vehicle:
    vehicle = await get_vehicle(db, vehicle_id)
    # Note: registration_number is intentionally NOT part of VehicleUpdate —
    # it's treated as immutable after creation. If that ever changes, add a
    # duplicate-check here the same way create_vehicle() does.
    update_data = vehicle_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(vehicle, field, value)

    if updated_by is not None:
        vehicle.updated_by = updated_by

    await db.commit()
    await db.refresh(vehicle)
    return vehicle


async def soft_delete_vehicle(db: AsyncSession, vehicle_id: int, updated_by: int | None = None) -> None:
    vehicle = await get_vehicle(db, vehicle_id)
    vehicle.is_deleted = True
    vehicle.deleted_at = datetime.utcnow()
    if updated_by is not None:
        vehicle.updated_by = updated_by
    await db.commit()