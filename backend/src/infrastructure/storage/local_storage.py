import asyncio

from src.core.config import Settings
from src.infrastructure.storage.base import BaseStorage, StoredFileInfo


class LocalStorage(BaseStorage):

    def __init__(self, settings: Settings):
        self.base_dir = settings.storage_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def write_file(self, name: str, content: bytes) -> StoredFileInfo:
        file_path = self.base_dir / name
        await asyncio.to_thread(file_path.write_bytes, content)

        return StoredFileInfo(path=file_path, size=len(content))

    async def read_file(self, stored_name: str) -> str:
        pass
