"""
app/schemas/dashboard.py

These aren't 1:1 table mirrors — they're computed/aggregated shapes returned
by app/services/dashboard_service.py (Phase 7) for the Admin Dashboard's
metric cards and charts (Recharts on the frontend).
"""

from pydantic import BaseModel, ConfigDict

from app.core.enums import DriverStatus, TripStatus, VehicleStatus


class VehicleStatusBreakdown(BaseModel):
    status: VehicleStatus
    count: int


class TripStatusBreakdown(BaseModel):
    status: TripStatus
    count: int


class DriverStatusBreakdown(BaseModel):
    status: DriverStatus
    count: int


class FleetUtilization(BaseModel):
    """Powers the 'fleet utilization' metric card."""

    total_vehicles: int
    vehicles_on_trip: int
    utilization_percent: float  # vehicles_on_trip / total_vehicles * 100, rounded


class DashboardSummary(BaseModel):
    """Top-level response for GET /api/v1/dashboard/summary"""

    model_config = ConfigDict(from_attributes=True)

    active_trips: int
    completed_trips_today: int
    planned_trips: int
    delayed_trips: int  # in-progress trips past their planned end/window

    total_vehicles: int
    total_drivers: int
    available_drivers: int

    fleet_utilization: FleetUtilization
    vehicle_status_breakdown: list[VehicleStatusBreakdown]
    trip_status_breakdown: list[TripStatusBreakdown]
    driver_status_breakdown: list[DriverStatusBreakdown]

    alerts: list[str] = []  # e.g. "3 vehicles overdue for maintenance"