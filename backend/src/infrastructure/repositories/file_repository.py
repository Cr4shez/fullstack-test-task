from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import StoredFile
from src.infrastructure.repositories.base import BaseRepository
from src.domain.schemas import FileCreateDTO, FileDTO


class FileRepository(BaseRepository[StoredFile, FileDTO, FileCreateDTO, FileDTO]):
    def __init__(self, session: AsyncSession):
        model = StoredFile
        schema = FileDTO
        super().__init__(model, schema, session)
