from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.urls import router as url_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(url_router, prefix="/api/v1")
