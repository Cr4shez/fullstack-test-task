from abc import ABC, abstractmethod
from pathlib import Path
from typing import NamedTuple


class StoredFileInfo(NamedTuple):
    path: Path
    size: int


class BaseStorage(ABC):
    @abstractmethod
    async def write_file(self, name:str, content: bytes) -> StoredFileInfo:
        """Сохраняет поток данных и возвращает информацию о файле."""
        pass

    @abstractmethod
    async def read_file(self, stored_name: str) -> str:
        pass
