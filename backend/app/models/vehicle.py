from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, Boolean, DateTime, Enum, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import VehicleStatus


class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.organization_id"), nullable=False
    )
    vehicle_type_id: Mapped[int] = mapped_column(
        ForeignKey("vehicle_types.vehicle_type_id"), nullable=False
    )

    vehicle_code: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    registration_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturing_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    maximum_load_capacity: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    odometer: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    acquisition_cost: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)

    vehicle_status: Mapped[VehicleStatus] = mapped_column(
        Enum(
            VehicleStatus,
            name="vehicle_status_enum",
            create_type=False,
        ),
        default=VehicleStatus.AVAILABLE,
        server_default=VehicleStatus.AVAILABLE.value,
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
        CheckConstraint("manufacturing_year >= 1980", name="check_manufacturing_year"),
        CheckConstraint("maximum_load_capacity >= 0", name="check_max_load_capacity"),
        CheckConstraint("odometer >= 0", name="check_odometer"),
        CheckConstraint("acquisition_cost >= 0", name="check_acquisition_cost"),
    )

    vehicle_type: Mapped["VehicleType"] = relationship(foreign_keys=[vehicle_type_id])