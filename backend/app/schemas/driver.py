"""
app/schemas/driver.py

Pydantic shapes for the `drivers` table. Mirrors app/models/driver.py exactly,
including the license_category CHECK constraint from the SQL schema.
"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import DriverStatus

# Matches the CHECK constraint on drivers.license_category in the SQL schema
ALLOWED_LICENSE_CATEGORIES = {"LMV", "HMV", "MCWG", "HPMV", "TRANS"}


class DriverBase(BaseModel):
    user_id: int
    license_number: str = Field(..., min_length=1, max_length=50)
    license_category: str | None = Field(None, max_length=20)
    license_expiry: date

    @field_validator("license_category")
    @classmethod
    def validate_license_category(cls, v: str | None) -> str | None:
        if v is not None and v not in ALLOWED_LICENSE_CATEGORIES:
            raise ValueError(
                f"license_category must be one of {sorted(ALLOWED_LICENSE_CATEGORIES)}"
            )
        return v


class DriverCreate(DriverBase):
    """Body for POST /api/v1/drivers — promotes an existing User to a Driver profile."""

    pass


class DriverUpdate(BaseModel):
    """Body for PATCH /api/v1/drivers/{id}. All fields optional."""

    license_number: str | None = Field(None, min_length=1, max_length=50)
    license_category: str | None = Field(None, max_length=20)
    license_expiry: date | None = None
    safety_score: Decimal | None = Field(None, ge=0, le=100)
    driver_status: DriverStatus | None = None

    @field_validator("license_category")
    @classmethod
    def validate_license_category(cls, v: str | None) -> str | None:
        if v is not None and v not in ALLOWED_LICENSE_CATEGORIES:
            raise ValueError(
                f"license_category must be one of {sorted(ALLOWED_LICENSE_CATEGORIES)}"
            )
        return v


class DriverStatusUpdate(BaseModel):
    """Lightweight schema for the Driver App view — just flipping availability."""

    driver_status: DriverStatus


class DriverRead(DriverBase):
    model_config = ConfigDict(from_attributes=True)

    driver_id: int
    safety_score: Decimal
    driver_status: DriverStatus
    created_by: int | None = None
    updated_by: int | None = None
    created_at: datetime
    updated_at: datetime