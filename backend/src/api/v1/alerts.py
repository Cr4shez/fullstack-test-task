from fastapi import APIRouter, Depends

from src.core.dependencies import AlertRepoDep
from src.domain.schemas.alerts import AlertResponse
from src.domain.schemas.base import PaginationParams, PaginatedResponse


alert_router = APIRouter()


@alert_router.get("/", response_model=PaginatedResponse[AlertResponse])
async def list_alerts_view(
    repo: AlertRepoDep,
    params: PaginationParams = Depends()
):
    items, total = await repo.find_all(limit=params.limit, offset=params.offset)
    return PaginatedResponse[AlertResponse](
        items=items,
        total=total,
        page=params.page,
        size=params.limit,
        has_next=(params.page * params.limit) < total
    )
