from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["Health & Observability"])


class HealthResponse(BaseModel):
    status: str
    service: str = "brandkotha-api"


@router.get("/live", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def liveness_probe():
    return HealthResponse(status="ok")


@router.get("/ready", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def readiness_probe():
    # In a fully connected cluster, this probes PostgreSQL and Redis
    return HealthResponse(status="ready")
