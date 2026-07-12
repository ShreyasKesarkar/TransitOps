from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, DateTime, Enum, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import TripStatus


class Trip(Base):
    __tablename__ = "trips"

    trip_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trip_code: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.organization_id"), nullable=False
    )
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.vehicle_id"), nullable=False)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.driver_id"), nullable=False)

    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)

    source: Mapped[str] = mapped_column(String(150), nullable=False)
    destination: Mapped[str] = mapped_column(String(150), nullable=False)

    cargo_weight: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    planned_distance: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    actual_distance: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    trip_status: Mapped[TripStatus] = mapped_column(
        Enum(
            TripStatus,
            name="trip_status_enum",
            create_type=False,
        ),
        default=TripStatus.PLANNED,
        server_default=TripStatus.PLANNED.value,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint("cargo_weight >= 0", name="check_cargo_weight"),
        CheckConstraint("planned_distance >= 0", name="check_planned_distance"),
        CheckConstraint("actual_distance >= 0", name="check_actual_distance"),
    )

    # Relationships — critical for this table specifically, since your
    # dashboard and trip list views will constantly need vehicle + driver
    # details alongside trip data (e.g. "show registration_number on trip card").
    vehicle: Mapped["Vehicle"] = relationship(foreign_keys=[vehicle_id])
    driver: Mapped["Driver"] = relationship(foreign_keys=[driver_id])