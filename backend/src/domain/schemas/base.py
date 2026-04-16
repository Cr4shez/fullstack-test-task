from typing import List, Any, Generic, T

from pydantic import BaseModel, computed_field, Field


class PaginationParams(BaseModel):
    limit: int = Field(10, ge=1)
    page: int = Field(1, ge=1)

    @computed_field
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[Any]
    total: int
    page: int
    size: int
    has_next: bool
