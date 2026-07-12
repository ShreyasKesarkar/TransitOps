from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import String, Date, Numeric, Boolean, DateTime, Enum, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import DriverStatus


class Driver(Base):
    __tablename__ = "drivers"

    driver_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), unique=True, nullable=False
    )

    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    license_category: Mapped[str | None] = mapped_column(String(20), nullable=True)
    license_expiry: Mapped[date] = mapped_column(Date, nullable=False)

    safety_score: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal("100.00"), server_default="100.00"
    )

    driver_status: Mapped[DriverStatus] = mapped_column(
        Enum(
            DriverStatus,
            name="driver_status_enum",
            create_type=False,
        ),
        default=DriverStatus.AVAILABLE,
        server_default=DriverStatus.AVAILABLE.value,
    )

    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "license_category IN ('LMV','HMV','MCWG','HPMV','TRANS')",
            name="check_license_category",
        ),
    )

    # One-to-one back to the user account this driver profile belongs to.
    user: Mapped["User"] = relationship(foreign_keys=[user_id])