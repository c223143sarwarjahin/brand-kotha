from fastapi import APIRouter
from app.api.v1 import health

api_router = APIRouter()

# Core health checks
api_router.include_router(health.router)

# Note: As domain service modules (auth, profiles, campaigns, pitches, chat, billing, admin)
# are implemented, their routers will be included here under /api/v1.

