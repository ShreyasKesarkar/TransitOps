from app.schemas.auth import LoginRequest, TokenResponse, TokenPayload
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserPasswordChange,
    UserRead,
    UserSummary,
)
from app.schemas.driver import (
    DriverBase,
    DriverCreate,
    DriverUpdate,
    DriverStatusUpdate,
    DriverRead,
)
from app.schemas.vehicle import (
    VehicleBase,
    VehicleCreate,
    VehicleUpdate,
    VehicleRead,
    VehicleSummary,
)
from app.schemas.trip import (
    TripBase,
    TripCreate,
    TripUpdate,
    TripStatusUpdate,
    TripRead,
    TripReadDetailed,
)
from app.schemas.dashboard import (
    VehicleStatusBreakdown,
    TripStatusBreakdown,
    DriverStatusBreakdown,
    FleetUtilization,
    DashboardSummary,
)

__all__ = [
    "LoginRequest",
    "TokenResponse",
    "TokenPayload",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPasswordChange",
    "UserRead",
    "UserSummary",
    "DriverBase",
    "DriverCreate",
    "DriverUpdate",
    "DriverStatusUpdate",
    "DriverRead",
    "VehicleBase",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleRead",
    "VehicleSummary",
    "TripBase",
    "TripCreate",
    "TripUpdate",
    "TripStatusUpdate",
    "TripRead",
    "TripReadDetailed",
    "VehicleStatusBreakdown",
    "TripStatusBreakdown",
    "DriverStatusBreakdown",
    "FleetUtilization",
    "DashboardSummary",
]