from pydantic import BaseModel, ConfigDict

from src.domain.schemas.mixins import partial, CreatedSchemaMixin
from src.domain.schemas.enums import AlertLevel


class AlertBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    file_id: str
    level: AlertLevel
    message: str


class AlertCreateRequest(AlertBase):
    pass


class AlertResponse(CreatedSchemaMixin, AlertBase):
    id: int


class AlertCreateDTO(AlertBase):
    pass


@partial
class AlertDTO(CreatedSchemaMixin, AlertBase):
    id: int

