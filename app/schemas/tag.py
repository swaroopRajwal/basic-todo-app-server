from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.api_request import PaginationParamsSchema, SortParamsSchema


class TagBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=40)


class TagResponse(TagBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagSortField(str, Enum):
    name = "name"
    created_at = "created_at"
    updated_at = "updated_at"


class TagQueryParamsSchema(PaginationParamsSchema, SortParamsSchema[TagSortField]):
    pass
