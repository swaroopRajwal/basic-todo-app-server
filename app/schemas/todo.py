from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from app.schemas.api_request import PaginationParamsSchema, SortParamsSchema
from app.schemas.tag import TagResponse


class TodoBase(BaseModel):
    title: str = Field(max_length=150, min_length=1)
    description: str | None = Field(default=None, max_length=1000)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=150, min_length=1)
    description: str | None = Field(default=None, max_length=1000)
    is_completed: bool | None = None
    tag_ids: list[str] | None = None


# Schema for returning a Todo from the API (includes DB-generated fields)
class TodoResponse(TodoBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_completed: bool = False
    tags: list[TagResponse] = Field(default_factory=list)

    # Pydantic V2 config to allow reading from SQLAlchemy ORM objects
    model_config = ConfigDict(from_attributes=True)


class TodoSortField(str, Enum):
    title = "title"
    created_at = "created_at"
    updated_at = "updated_at"


class TodoQueryParamsSchema(PaginationParamsSchema, SortParamsSchema[TodoSortField]):
    is_completed: bool | None = None
