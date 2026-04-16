from typing import TYPE_CHECKING

from src.domain.exceptions import FileMissingError
from src.domain.logic import determine_file_alert
from src.domain.schemas import AlertCreateDTO

if TYPE_CHECKING:
    from src.infrastructure.repositories.alert_repository import AlertRepository
    from src.infrastructure.repositories.file_repository import FileRepository


class AlertUseCases:
    def __init__(
        self,
        file_repo: FileRepository,
        alert_repo: AlertRepository,
    ):
        self.file_repo = file_repo
        self.repo = alert_repo

    async def create_file_alert(self, file_id: str) -> None:
        file_item = await self.file_repo.find_by_id(file_id)

        if not file_item:
            raise FileMissingError()

        alert = determine_file_alert(file_item)

        await self.repo.create(AlertCreateDTO(
            file_id=file_id,
            level=alert.level,
            message=alert.message
        ))
