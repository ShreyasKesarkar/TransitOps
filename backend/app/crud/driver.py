"""
app/crud/driver.py

Data-access layer for the `drivers` table.
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.enums import DriverStatus
from app.crud.exceptions import DuplicateError, NotFoundError
from app.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverUpdate


async def get_driver(db: AsyncSession, driver_id: int) -> Driver:
    result = await db.execute(
        select(Driver)
        .options(selectinload(Driver.user))
        .where(Driver.driver_id == driver_id, Driver.is_deleted.is_(False))
    )
    driver = result.scalar_one_or_none()
    if driver is None:
        raise NotFoundError(f"Driver {driver_id} not found")
    return driver


async def get_driver_by_user_id(db: AsyncSession, user_id: int) -> Driver | None:
    result = await db.execute(
        select(Driver).where(Driver.user_id == user_id, Driver.is_deleted.is_(False))
    )
    return result.scalar_one_or_none()


async def get_driver_by_license_number(db: AsyncSession, license_number: str) -> Driver | None:
    result = await db.execute(
        select(Driver).where(
            Driver.license_number == license_number, Driver.is_deleted.is_(False)
        )
    )
    return result.scalar_one_or_none()


async def get_drivers(
    db: AsyncSession,
    status: DriverStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Driver]:
    stmt = select(Driver).options(selectinload(Driver.user)).where(Driver.is_deleted.is_(False))
    if status is not None:
        stmt = stmt.where(Driver.driver_status == status)
    stmt = stmt.offset(skip).limit(limit).order_by(Driver.driver_id)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_driver(
    db: AsyncSession, driver_in: DriverCreate, created_by: int | None = None
) -> Driver:
    existing_profile = await get_driver_by_user_id(db, driver_in.user_id)
    if existing_profile is not None:
        raise DuplicateError(f"User {driver_in.user_id} already has a driver profile")

    existing_license = await get_driver_by_license_number(db, driver_in.license_number)
    if existing_license is not None:
        raise DuplicateError(f"License number '{driver_in.license_number}' is already registered")

    driver = Driver(
        user_id=driver_in.user_id,
        license_number=driver_in.license_number,
        license_category=driver_in.license_category,
        license_expiry=driver_in.license_expiry,
        created_by=created_by,
    )
    db.add(driver)
    await db.commit()
    await db.refresh(driver)
    return driver


async def update_driver(
    db: AsyncSession, driver_id: int, driver_in: DriverUpdate, updated_by: int | None = None
) -> Driver:
    driver = await get_driver(db, driver_id)
    update_data = driver_in.model_dump(exclude_unset=True)

    if "license_number" in update_data and update_data["license_number"] != driver.license_number:
        existing = await get_driver_by_license_number(db, update_data["license_number"])
        if existing is not None:
            raise DuplicateError(
                f"License number '{update_data['license_number']}' is already registered"
            )

    for field, value in update_data.items():
        setattr(driver, field, value)

    if updated_by is not None:
        driver.updated_by = updated_by

    await db.commit()
    await db.refresh(driver)
    return driver


async def soft_delete_driver(db: AsyncSession, driver_id: int, updated_by: int | None = None) -> None:
    driver = await get_driver(db, driver_id)
    driver.is_deleted = True
    driver.deleted_at = datetime.utcnow()
    if updated_by is not None:
        driver.updated_by = updated_by
    await db.commit()