from fastapi import APIRouter

from app.api.endpoints import assistant

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(assistant.router, prefix="/assistant", tags=["assistant"])
