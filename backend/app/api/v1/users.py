"""
app/api/v1/users.py

CRUD routes for the `users` table. Admin-only for writes; any authenticated
user can read (list is still org-scoped by query param since we don't have
row-level org scoping baked into deps yet).
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, require_roles
from app.core.database import get_db
from app.crud import user as user_crud
from app.crud.exceptions import DuplicateError, NotFoundError
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserRead])
async def list_users(
    organization_id: int | None = Query(None),
    role_id: int | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[User]:
    return await user_crud.get_users(
        db, organization_id=organization_id, role_id=role_id, skip=skip, limit=limit
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> User:
    try:
        return await user_crud.get_user(db, user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("Admin"))],
)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> User:
    try:
        return await user_crud.create_user(db, user_in, created_by=current_user.user_id)
    except DuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_roles("Admin"))],
)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> User:
    try:
        return await user_crud.update_user(db, user_id, user_in, updated_by=current_user.user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles("Admin"))],
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    try:
        await user_crud.soft_delete_user(db, user_id, updated_by=current_user.user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc