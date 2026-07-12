"""
app/api/deps.py  (Phase 7 update)

Shared FastAPI dependencies used across every protected route:
- get_db                      re-exported from app.core.database
- get_current_user            decodes the bearer token -> loads the User row
- get_current_active_user     additionally enforces employment_status == ACTIVE
- get_role_name                looks up a role_id's name fresh from the DB
- require_roles(*names)        dependency factory for role-based access control
- translate_crud_errors()      async context manager: NotFoundError -> 404, DuplicateError -> 409

CHANGE FROM PHASE 5: added get_role_name() and translate_crud_errors().
require_roles() now calls get_role_name() internally instead of duplicating
the query, and the Phase 7 route files (users/drivers/vehicles/trips) use
both of these directly for ownership checks and error handling.
"""

from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.enums import EmploymentStatus
from app.core.security import decode_access_token
from app.crud.exceptions import DuplicateError, NotFoundError
from app.models.role import Role
from app.models.user import User

# tokenUrl is only used to populate the "Authorize" button in Swagger UI —
# the actual login route logic lives in app/api/v1/auth.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Decode the JWT, then load the matching, non-deleted user row."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    raw_user_id = payload.get("sub")
    if raw_user_id is None:
        raise credentials_exception

    try:
        user_id = int(raw_user_id)
    except (TypeError, ValueError):
        raise credentials_exception

    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if user is None or user.is_deleted:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Extra guard on top of get_current_user: blocks inactive/suspended/resigned accounts."""
    if current_user.employment_status != EmploymentStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active",
        )
    return current_user


async def get_role_name(db: AsyncSession, role_id: int) -> str | None:
    """
    Looks up a role's name fresh from the DB (not from the JWT claim) so that
    a role change takes effect immediately. Used by require_roles() below and
    directly by route files for ownership-vs-role checks (e.g. "is this the
    driver's own trip, OR are they a Fleet Manager").
    """
    result = await db.execute(select(Role.role_name).where(Role.role_id == role_id))
    return result.scalar_one_or_none()


def require_roles(*allowed_roles: str):
    """
    Dependency factory for role-based access control.

    Usage:
        @router.post("/vehicles", dependencies=[Depends(require_roles("Admin", "Fleet Manager"))])
    """

    async def role_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_db)],
    ) -> User:
        role_name = await get_role_name(db, current_user.role_id)

        if role_name is None or role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {', '.join(allowed_roles)}",
            )
        return current_user

    return role_checker


@asynccontextmanager
async def translate_crud_errors() -> AsyncIterator[None]:
    """
    Wrap a CRUD call so its domain exceptions become proper HTTP responses:
        NotFoundError  -> 404
        DuplicateError -> 409

    Usage:
        async with translate_crud_errors():
            user = await crud.user.get_user(db, user_id)
    """
    try:
        yield
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc