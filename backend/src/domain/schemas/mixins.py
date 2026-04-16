from typing import TypeVar, Type
import datetime as dt

from pydantic import BaseModel, create_model

ModelT = TypeVar("ModelT", bound=Type[BaseModel])


def partial(model: ModelT) -> ModelT:
    """Декоратор, который делает все поля Pydantic-модели необязательными."""

    partial_fields = {
        name: (field.annotation | None, None)
        for name, field in model.model_fields.items()
    }

    return create_model(
        model.__name__,
        __base__=model,
        **partial_fields
    )


class CreatedSchemaMixin(BaseModel):
    created_at: dt.datetime


class UpdatedSchemaMixin(BaseModel):
    updated_at: dt.datetime


class TimestampSchemaMixin(CreatedSchemaMixin, UpdatedSchemaMixin):
    pass
