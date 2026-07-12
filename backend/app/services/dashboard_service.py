"""
app/services/dashboard_service.py

Aggregation queries powering the Admin Dashboard (GET /api/v1/dashboard/summary).
Everything here is read-only, computed on the fly from trips/vehicles/drivers —
no dedicated summary table.

Note on "delayed_trips": the SQL schema has no planned_end_time / scheduled
duration column on trips, so there's no exact way to know a trip is "late".
As a reasonable proxy, a trip is treated as delayed if it's still IN_PROGRESS
and has been running longer than DELAYED_TRIP_THRESHOLD_HOURS since start_time.
Swap this out for a real SLA field if one gets added to the schema later.
"""

from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import DriverStatus, TripStatus, VehicleStatus
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.schemas.dashboard import (
    DashboardSummary,
    DriverStatusBreakdown,
    FleetUtilization,
    TripStatusBreakdown,
    VehicleStatusBreakdown,
)

DELAYED_TRIP_THRESHOLD_HOURS = 4


async def _count_trips_by_status(db: AsyncSession, organization_id: int | None) -> dict[TripStatus, int]:
    stmt = select(Trip.trip_status, func.count(Trip.trip_id)).group_by(Trip.trip_status)
    if organization_id is not None:
        stmt = stmt.where(Trip.organization_id == organization_id)
    result = await db.execute(stmt)
    return {row[0]: row[1] for row in result.all()}


async def _count_vehicles_by_status(
    db: AsyncSession, organization_id: int | None
) -> dict[VehicleStatus, int]:
    stmt = (
        select(Vehicle.vehicle_status, func.count(Vehicle.vehicle_id))
        .where(Vehicle.is_deleted.is_(False))
        .group_by(Vehicle.vehicle_status)
    )
    if organization_id is not None:
        stmt = stmt.where(Vehicle.organization_id == organization_id)
    result = await db.execute(stmt)
    return {row[0]: row[1] for row in result.all()}


async def _count_drivers_by_status(db: AsyncSession) -> dict[DriverStatus, int]:
    # drivers table has no organization_id column directly (it hangs off users),
    # so this is platform-wide unless/until that scoping is added.
    stmt = (
        select(Driver.driver_status, func.count(Driver.driver_id))
        .where(Driver.is_deleted.is_(False))
        .group_by(Driver.driver_status)
    )
    result = await db.execute(stmt)
    return {row[0]: row[1] for row in result.all()}


async def _count_completed_trips_today(db: AsyncSession, organization_id: int | None) -> int:
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    stmt = select(func.count(Trip.trip_id)).where(
        Trip.trip_status == TripStatus.COMPLETED,
        Trip.end_time.is_not(None),
        Trip.end_time >= today_start,
    )
    if organization_id is not None:
        stmt = stmt.where(Trip.organization_id == organization_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def _count_delayed_trips(db: AsyncSession, organization_id: int | None) -> int:
    cutoff = datetime.utcnow() - timedelta(hours=DELAYED_TRIP_THRESHOLD_HOURS)
    stmt = select(func.count(Trip.trip_id)).where(
        Trip.trip_status == TripStatus.IN_PROGRESS,
        Trip.start_time.is_not(None),
        Trip.start_time <= cutoff,
    )
    if organization_id is not None:
        stmt = stmt.where(Trip.organization_id == organization_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_dashboard_summary(
    db: AsyncSession, organization_id: int | None = None
) -> DashboardSummary:
    trip_counts = await _count_trips_by_status(db, organization_id)
    vehicle_counts = await _count_vehicles_by_status(db, organization_id)
    driver_counts = await _count_drivers_by_status(db)

    completed_trips_today = await _count_completed_trips_today(db, organization_id)
    delayed_trips = await _count_delayed_trips(db, organization_id)

    total_vehicles = sum(vehicle_counts.values())
    vehicles_on_trip = vehicle_counts.get(VehicleStatus.ON_TRIP, 0)
    utilization_percent = (
        round((vehicles_on_trip / total_vehicles) * 100, 2) if total_vehicles else 0.0
    )

    total_drivers = sum(driver_counts.values())
    available_drivers = driver_counts.get(DriverStatus.AVAILABLE, 0)

    alerts: list[str] = []
    vehicles_in_maintenance = vehicle_counts.get(VehicleStatus.IN_MAINTENANCE, 0)
    if vehicles_in_maintenance:
        alerts.append(f"{vehicles_in_maintenance} vehicle(s) currently in maintenance")
    if delayed_trips:
        alerts.append(f"{delayed_trips} trip(s) running longer than expected")
    suspended_drivers = driver_counts.get(DriverStatus.SUSPENDED, 0)
    if suspended_drivers:
        alerts.append(f"{suspended_drivers} driver(s) suspended")

    return DashboardSummary(
        active_trips=trip_counts.get(TripStatus.IN_PROGRESS, 0),
        completed_trips_today=completed_trips_today,
        planned_trips=trip_counts.get(TripStatus.PLANNED, 0),
        delayed_trips=delayed_trips,
        total_vehicles=total_vehicles,
        total_drivers=total_drivers,
        available_drivers=available_drivers,
        fleet_utilization=FleetUtilization(
            total_vehicles=total_vehicles,
            vehicles_on_trip=vehicles_on_trip,
            utilization_percent=utilization_percent,
        ),
        vehicle_status_breakdown=[
            VehicleStatusBreakdown(status=s, count=c) for s, c in vehicle_counts.items()
        ],
        trip_status_breakdown=[
            TripStatusBreakdown(status=s, count=c) for s, c in trip_counts.items()
        ],
        driver_status_breakdown=[
            DriverStatusBreakdown(status=s, count=c) for s, c in driver_counts.items()
        ],
        alerts=alerts,
    )