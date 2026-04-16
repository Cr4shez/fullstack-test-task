from fastapi import APIRouter

from src.api.v1.alerts import alert_router
from src.api.v1.files import file_router


base_router = APIRouter(prefix="/api/v1")

base_router.include_router(file_router, prefix="/files")
base_router.include_router(alert_router, prefix="/alerts")
