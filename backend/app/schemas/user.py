"""
app/schemas/user.py

Pydantic shapes for the `users` table. Mirrors app/models/user.py exactly.
Note: password_hash is never exposed in any Read schema.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import EmploymentStatus


class UserBase(BaseModel):
    organization_id: int
    role_id: int
    employee_code: str | None = Field(None, max_length=20)
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(None, max_length=15)


class UserCreate(UserBase):
    """Body for POST /api/v1/users — plaintext password, hashed by the service layer."""

    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Body for PATCH /api/v1/users/{id}. All fields optional (partial update)."""

    role_id: int | None = None
    employee_code: str | None = Field(None, max_length=20)
    full_name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=15)
    employment_status: EmploymentStatus | None = None


class UserPasswordChange(BaseModel):
    """Body for a dedicated change-password endpoint."""

    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)


class UserRead(UserBase):
    """Response shape — safe to return to clients, no password fields."""

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    employment_status: EmploymentStatus
    must_change_password: bool
    created_by: int | None = None
    updated_by: int | None = None
    created_at: datetime
    updated_at: datetime


class UserSummary(BaseModel):
    """Minimal shape for embedding inside other responses (e.g. TripRead.driver.user)."""

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    full_name: str
    email: EmailStr