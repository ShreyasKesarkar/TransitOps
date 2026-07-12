"""
app/crud/trip.py

Data-access layer for the `trips` table.

IMPORTANT: unlike users/drivers/vehicles, the `trips` table has NO
is_deleted / deleted_at columns in the SQL schema — so delete_trip()
below is a genuine hard DELETE, not a soft-delete flag flip.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.enums import TripStatus
from app.crud.exceptions import DuplicateError, NotFoundError
from app.models.trip import Trip
from app.schemas.trip import TripCreate, TripUpdate


async def get_trip(db: AsyncSession, trip_id: int) -> Trip:
    result = await db.execute(
        select(Trip)
        .options(selectinload(Trip.vehicle), selectinload(Trip.driver))
        .where(Trip.trip_id == trip_id)
    )
    trip = result.scalar_one_or_none()
    if trip is None:
        raise NotFoundError(f"Trip {trip_id} not found")
    return trip


async def get_trip_by_code(db: AsyncSession, trip_code: str) -> Trip | None:
    result = await db.execute(select(Trip).where(Trip.trip_code == trip_code))
    return result.scalar_one_or_none()


async def get_trips(
    db: AsyncSession,
    organization_id: int | None = None,
    status: TripStatus | None = None,
    driver_id: int | None = None,
    vehicle_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Trip]:
    stmt = select(Trip).options(selectinload(Trip.vehicle), selectinload(Trip.driver))

    if organization_id is not None:
        stmt = stmt.where(Trip.organization_id == organization_id)
    if status is not None:
        stmt = stmt.where(Trip.trip_status == status)
    if driver_id is not None:
        stmt = stmt.where(Trip.driver_id == driver_id)
    if vehicle_id is not None:
        stmt = stmt.where(Trip.vehicle_id == vehicle_id)

    stmt = stmt.offset(skip).limit(limit).order_by(Trip.trip_id.desc())

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_trip(db: AsyncSession, trip_in: TripCreate, created_by: int | None = None) -> Trip:
    if trip_in.trip_code is not None:
        existing = await get_trip_by_code(db, trip_in.trip_code)
        if existing is not None:
            raise DuplicateError(f"Trip code '{trip_in.trip_code}' is already in use")

    trip = Trip(
        trip_code=trip_in.trip_code,
        organization_id=trip_in.organization_id,
        vehicle_id=trip_in.vehicle_id,
        driver_id=trip_in.driver_id,
        source=trip_in.source,
        destination=trip_in.destination,
        cargo_weight=trip_in.cargo_weight,
        planned_distance=trip_in.planned_distance,
        created_by=created_by,
    )
    db.add(trip)
    await db.commit()
    await db.refresh(trip)
    return trip


async def update_trip(
    db: AsyncSession, trip_id: int, trip_in: TripUpdate, updated_by: int | None = None
) -> Trip:
    """
    General-purpose update for dispatcher edits: reassigning vehicle/driver,
    correcting source/destination, recording actual_distance/start/end time,
    or changing trip_status. TripUpdate.check_end_after_start() already
    validates end_time >= start_time at the schema level.
    """
    trip = await get_trip(db, trip_id)
    update_data = trip_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(trip, field, value)

    if updated_by is not None:
        trip.updated_by = updated_by

    await db.commit()
    await db.refresh(trip)
    return trip


async def update_trip_status(
    db: AsyncSession, trip_id: int, new_status: TripStatus, updated_by: int | None = None
) -> Trip:
    """
    Lightweight status-only update — this is what the Driver App view
    calls (scheduled -> in-progress -> completed) without needing to
    send the full trip payload.
    """
    trip = await get_trip(db, trip_id)
    trip.trip_status = new_status
    if updated_by is not None:
        trip.updated_by = updated_by
    await db.commit()
    await db.refresh(trip)
    return trip


async def delete_trip(db: AsyncSession, trip_id: int) -> None:
    """Hard delete — see module docstring for why this differs from the other CRUD modules."""
    trip = await get_trip(db, trip_id)
    await db.delete(trip)
    await db.commit()