from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import EmploymentStatus


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.organization_id"), nullable=False
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"), nullable=False)

    employee_code: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    must_change_password: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")

    employment_status: Mapped[EmploymentStatus] = mapped_column(
        Enum(
            EmploymentStatus,
            name="employment_status_enum",
            create_type=False,
        ),
        default=EmploymentStatus.ACTIVE,
        server_default=EmploymentStatus.ACTIVE.value,
    )

    # Self-referencing audit columns — who created/updated this user.
    # No ORM relationship() defined for these on purpose (see note below).
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships to parent tables — lets us do user.organization.organization_name
    # instead of a manual second query.
    organization: Mapped["Organization"] = relationship(foreign_keys=[organization_id])
    role: Mapped["Role"] = relationship(foreign_keys=[role_id])