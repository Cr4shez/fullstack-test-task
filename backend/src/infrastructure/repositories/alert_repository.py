from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import Alert
from src.infrastructure.repositories.base import BaseRepository
from src.domain.schemas import AlertCreateDTO, AlertDTO


class AlertRepository(BaseRepository[Alert, AlertDTO, AlertCreateDTO, AlertDTO]):
    def __init__(self, session: AsyncSession):
        model = Alert
        schema = AlertDTO
        super().__init__(model, schema, session)
