"""
app/services/auth_service.py

Login business logic: verify credentials, enforce account-status rules,
and mint a JWT. Kept separate from the route (app/api/v1/auth.py) so it
can be unit-tested without spinning up FastAPI, and reused elsewhere later
(e.g. a future password-reset flow).
"""

from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.enums import EmploymentStatus
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse


class AuthError(Exception):
    """
    Raised for any login failure (unknown email, bad password, inactive account).
    Deliberately generic in message so the route layer can return a single
    401 without leaking which part of the check failed (avoids user enumeration).
    """


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    """
    Look up a user by email and validate their password + account status.
    Raises AuthError on any failure. Returns the ORM User on success,
    with `role` and `organization` eagerly loaded for use by the caller.
    """
    result = await db.execute(
        select(User)
        .options(selectinload(User.role), selectinload(User.organization))
        .where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if user is None or user.is_deleted:
        raise AuthError("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise AuthError("Invalid email or password")

    if user.employment_status != EmploymentStatus.ACTIVE:
        raise AuthError("This account is not active. Contact your administrator.")

    return user


async def login(db: AsyncSession, credentials: LoginRequest) -> TokenResponse:
    """
    Full login flow: authenticate, then issue a signed JWT carrying
    user_id, organization_id, role_id, and role_name as claims.
    """
    user = await authenticate_user(db, credentials.email, credentials.password)

    token_claims = {
        "sub": str(user.user_id),
        "organization_id": user.organization_id,
        "role_id": user.role_id,
        "role_name": user.role.role_name if user.role else None,
    }

    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=token_claims, expires_delta=expires_delta)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )