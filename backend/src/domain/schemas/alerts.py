from pydantic import BaseModel, ConfigDict

from src.domain.schemas.mixins import partial, CreatedSchemaMixin


class AlertCreateRequest(BaseModel):
    pass


class AlertResponse(BaseModel):
    pass


class AlertDTOBase(CreatedSchemaMixin, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_id: str
    level: str
    message: str


class AlertCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    file_id: str
    level: str
    message: str


@partial
class AlertDTO(AlertDTOBase):
    pass
