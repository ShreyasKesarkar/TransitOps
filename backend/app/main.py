"""
app/main.py

FastAPI application entrypoint. Creates the app, wires up CORS for the
Vite frontend, mounts the aggregated v1 router, and exposes a couple of
plain health-check endpoints for quick sanity testing.

Run with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Enterprise Smart Transport Operations Platform — backend API",
)

# CORS — allows the React/Vite frontend (localhost:5173 by default) to call
# this API from the browser. Origins are configurable via settings.CORS_ORIGINS
# (see app/core/config.py / .env) instead of being hardcoded here.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Health"])
async def root() -> dict:
    """Basic liveness check — confirms the app booted and is serving requests."""
    return {
        "service": settings.PROJECT_NAME,
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health() -> dict:
    """Health-check endpoint, e.g. for Docker healthchecks or uptime monitors."""
    return {"status": "healthy"}