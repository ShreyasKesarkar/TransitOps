"""
app/schemas/vehicle.py

Pydantic shapes for the `vehicles` table. Mirrors app/models/vehicle.py exactly,
including the CHECK constraints from the SQL schema (manufacturing_year >= 1980, etc.)
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import VehicleStatus


class VehicleBase(BaseModel):
    organization_id: int
    vehicle_type_id: int
    vehicle_code: str | None = Field(None, max_length=20)
    registration_number: str = Field(..., min_length=1, max_length=20)
    manufacturer: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    manufacturing_year: int | None = Field(None, ge=1980)
    maximum_load_capacity: Decimal | None = Field(None, ge=0)
    acquisition_cost: Decimal | None = Field(None, ge=0)


class VehicleCreate(VehicleBase):
    """Body for POST /api/v1/vehicles"""

    odometer: int = Field(0, ge=0)


class VehicleUpdate(BaseModel):
    """Body for PATCH /api/v1/vehicles/{id}. All fields optional."""

    vehicle_type_id: int | None = None
    vehicle_code: str | None = Field(None, max_length=20)
    manufacturer: str | None = Field(None, min_length=1, max_length=100)
    model: str | None = Field(None, min_length=1, max_length=100)
    manufacturing_year: int | None = Field(None, ge=1980)
    maximum_load_capacity: Decimal | None = Field(None, ge=0)
    odometer: int | None = Field(None, ge=0)
    acquisition_cost: Decimal | None = Field(None, ge=0)
    vehicle_status: VehicleStatus | None = None


class VehicleRead(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    vehicle_id: int
    odometer: int
    vehicle_status: VehicleStatus
    created_by: int | None = None
    updated_by: int | None = None
    created_at: datetime
    updated_at: datetime


class VehicleSummary(BaseModel):
    """Minimal shape for embedding inside TripRead / map markers."""

    model_config = ConfigDict(from_attributes=True)

    vehicle_id: int
    registration_number: str
    vehicle_status: VehicleStatus