from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: UUID


class DateMixin(BaseModel):
    modified: datetime
