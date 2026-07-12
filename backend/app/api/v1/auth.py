"""
app/api/v1/auth.py

Auth routes. Only /login is required for Phase 5; /me is included as a
free bonus endpoint since it's a one-line way to prove the whole
token -> get_current_user chain actually works end-to-end.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserRead
from app.services.auth_service import AuthError
from app.services.auth_service import login as perform_login

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate with email + password, get back a JWT access token.
    Frontend: POST JSON { "email": ..., "password": ... } to this route.
    """
    try:
        return await perform_login(db, credentials)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Returns the logged-in user's own profile. Useful for a quick sanity check."""
    return current_user