from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.responses import FileResponse as FastApiFileResponse

from src.core.dependencies import FileRepoDep, FileServiceDep
from src.domain.schemas.base import PaginatedResponse, PaginationParams
from src.domain.schemas.files import FileCreateRequest, FileUpdateRequest
from src.domain.schemas import FileResponse, FileDTO

file_router = APIRouter()


@file_router.get("/", response_model=PaginatedResponse[FileResponse])
async def list_files_view(repo: FileRepoDep, params: PaginationParams=Depends()):
    items = await repo.find_all(limit=params.limit, offset=params.offset)
    total = await repo.count()
    return PaginatedResponse[FileResponse](
        items=items,
        total=total,
        page=params.page,
        limit=params.limit,
        has_next=(params.page * params.limit) < total
    )


@file_router.post("/", response_model=FileResponse, status_code=201)
async def create_file_view(data: Annotated[FileCreateRequest, Form()], service: FileServiceDep):
    return await service.create_file_and_schedule_scan(
        FileDTO(title=data.title, file=data.file)
    )


@file_router.post("/{file_id}/scan")
async def scan_file(file_id: str, service: FileServiceDep):
    return await service.scan_for_threats(file_id)


@file_router.get("/{file_id}", response_model=FileResponse, status_code=200)
async def get_file_view(file_id: str, service: FileServiceDep):
    return await service.get_file(file_id)


@file_router.patch("/{file_id}", response_model=FileResponse)
async def update_file_view(
    file_id: str,
    payload: FileUpdateRequest,
    service: FileServiceDep
):
    return await service.update_file(file_id, FileDTO(title=payload.title))


@file_router.delete("/{file_id}", status_code=204)
async def delete_file_view(file_id: str, service: FileServiceDep):
    await service.delete_file(file_id)


@file_router.get("/{file_id}/download")
async def download_file(file_id: str, service: FileServiceDep):
    file_dto = await service.get_file(file_id)
    return FastApiFileResponse(
        path=file_dto.absolute_path,
        media_type=file_dto.mime_type,
        filename=file_dto.original_name,
    )
