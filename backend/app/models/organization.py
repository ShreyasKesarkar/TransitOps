from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.enums import OrganizationStatus


class Organization(Base):
    __tablename__ = "organizations"

    organization_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    organization_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    organization_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)

    organization_status: Mapped[OrganizationStatus] = mapped_column(
        Enum(
            OrganizationStatus,
            name="organization_status_enum",
            create_type=False,
        ),
        default=OrganizationStatus.ACTIVE,
        server_default=OrganizationStatus.ACTIVE.value,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)