"""
app/schemas/trip.py

Pydantic shapes for the `trips` table. Mirrors app/models/trip.py exactly.
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.enums import TripStatus
from app.schemas.driver import DriverRead
from app.schemas.vehicle import VehicleSummary


class TripBase(BaseModel):
    organization_id: int
    vehicle_id: int
    driver_id: int
    source: str = Field(..., min_length=1, max_length=150)
    destination: str = Field(..., min_length=1, max_length=150)
    cargo_weight: Decimal | None = Field(None, ge=0)
    planned_distance: Decimal | None = Field(None, ge=0)


class TripCreate(TripBase):
    """Body for POST /api/v1/trips — created by a Dispatcher/Admin."""

    trip_code: str | None = Field(None, max_length=20)


class TripUpdate(BaseModel):
    """
    Body for PATCH /api/v1/trips/{id}. All fields optional.
    Covers dispatcher edits (reassigning vehicle/driver) as well as
    trip progress fields (actual_distance, start_time, end_time, status).
    """

    vehicle_id: int | None = None
    driver_id: int | None = None
    source: str | None = Field(None, min_length=1, max_length=150)
    destination: str | None = Field(None, min_length=1, max_length=150)
    cargo_weight: Decimal | None = Field(None, ge=0)
    planned_distance: Decimal | None = Field(None, ge=0)
    actual_distance: Decimal | None = Field(None, ge=0)
    start_time: datetime | None = None
    end_time: datetime | None = None
    trip_status: TripStatus | None = None

    @model_validator(mode="after")
    def check_end_after_start(self) -> "TripUpdate":
        if self.start_time and self.end_time and self.end_time < self.start_time:
            raise ValueError("end_time cannot be earlier than start_time")
        return self


class TripStatusUpdate(BaseModel):
    """
    Lightweight schema for the Driver App view — just flipping a trip's status
    (e.g. scheduled -> in-progress -> completed) without touching other fields.
    """

    trip_status: TripStatus


class TripRead(TripBase):
    model_config = ConfigDict(from_attributes=True)

    trip_id: int
    trip_code: str | None = None
    actual_distance: Decimal | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    trip_status: TripStatus
    created_by: int | None = None
    updated_by: int | None = None
    created_at: datetime
    updated_at: datetime


class TripReadDetailed(TripRead):
    """
    Expanded response for the Dispatcher Console / Trip detail page —
    embeds vehicle and driver summaries so the frontend doesn't need
    3 separate round trips to render a single trip card.
    """

    vehicle: VehicleSummary | None = None
    driver: DriverRead | None = None