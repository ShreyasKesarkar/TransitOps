"""
app/api/v1/router.py

Aggregates every v1 sub-router into a single APIRouter that app/main.py
(Phase 8) mounts once under settings.API_V1_PREFIX.
"""

from fastapi import APIRouter

from app.api.v1 import auth, dashboard, drivers, trips, users, vehicles

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(drivers.router)
api_router.include_router(vehicles.router)
api_router.include_router(trips.router)
api_router.include_router(dashboard.router)