from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class VehicleType(Base):
    __tablename__ = "vehicle_types"

    vehicle_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    type_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)