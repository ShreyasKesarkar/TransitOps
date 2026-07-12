"""
app/crud/user.py

Data-access layer for the `users` table. No FastAPI/HTTP concerns here —
just SQLAlchemy queries and the domain rules that don't belong in the
route layer (uniqueness checks, soft-delete semantics).
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import hash_password
from app.crud.exceptions import DuplicateError, NotFoundError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user(db: AsyncSession, user_id: int) -> User:
    """Fetch one non-deleted user by PK, with role + organization eagerly loaded."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.role), selectinload(User.organization))
        .where(User.user_id == user_id, User.is_deleted.is_(False))
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise NotFoundError(f"User {user_id} not found")
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Returns None (not an exception) — used both for auth lookups and duplicate checks."""
    result = await db.execute(
        select(User).where(User.email == email, User.is_deleted.is_(False))
    )
    return result.scalar_one_or_none()


async def get_users(
    db: AsyncSession,
    organization_id: int | None = None,
    role_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    stmt = select(User).options(selectinload(User.role)).where(User.is_deleted.is_(False))
    if organization_id is not None:
        stmt = stmt.where(User.organization_id == organization_id)
    if role_id is not None:
        stmt = stmt.where(User.role_id == role_id)
    stmt = stmt.offset(skip).limit(limit).order_by(User.user_id)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_user(db: AsyncSession, user_in: UserCreate, created_by: int | None = None) -> User:
    existing = await get_user_by_email(db, user_in.email)
    if existing is not None:
        raise DuplicateError(f"A user with email '{user_in.email}' already exists")

    user = User(
        organization_id=user_in.organization_id,
        role_id=user_in.role_id,
        employee_code=user_in.employee_code,
        full_name=user_in.full_name,
        email=user_in.email,
        phone=user_in.phone,
        password_hash=hash_password(user_in.password),
        created_by=created_by,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(
    db: AsyncSession, user_id: int, user_in: UserUpdate, updated_by: int | None = None
) -> User:
    user = await get_user(db, user_id)
    update_data = user_in.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] != user.email:
        existing = await get_user_by_email(db, update_data["email"])
        if existing is not None:
            raise DuplicateError(f"A user with email '{update_data['email']}' already exists")

    for field, value in update_data.items():
        setattr(user, field, value)

    if updated_by is not None:
        user.updated_by = updated_by

    await db.commit()
    await db.refresh(user)
    return user


async def soft_delete_user(db: AsyncSession, user_id: int, updated_by: int | None = None) -> None:
    """Sets is_deleted=True + deleted_at instead of an actual DELETE, per the SQL schema's soft-delete columns."""
    user = await get_user(db, user_id)
    user.is_deleted = True
    user.deleted_at = datetime.utcnow()
    if updated_by is not None:
        user.updated_by = updated_by
    await db.commit()