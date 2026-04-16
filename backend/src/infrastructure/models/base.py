from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase, declarative_mixin


class Base(DeclarativeBase):
    pass

@declarative_mixin
class CreatedAtMixin:
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

@declarative_mixin
class UpdatedAtMixin:
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

@declarative_mixin
class TimestampMixin(CreatedAtMixin, UpdatedAtMixin):
    pass
