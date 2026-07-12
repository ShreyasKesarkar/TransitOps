"""
app/schemas/auth.py

Request/response shapes for the auth flow (Phase 5 will consume these).
"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Body for POST /api/v1/auth/login"""

    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Returned on successful login."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until expiry, mirrors settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


class TokenPayload(BaseModel):
    """
    Shape of the claims we encode into the JWT and decode back out of it.
    Used internally by app/api/deps.py (Phase 5) to build the current-user context.
    """

    sub: str  # user_id, stored as string per JWT "sub" convention
    organization_id: int
    role_id: int
    role_name: str | None = None
    exp: int | None = None