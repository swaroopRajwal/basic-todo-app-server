from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

SortFieldT = TypeVar("SortFieldT", bound=Enum)


class PaginationParamsSchema(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    search: str | None = None


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class SortParamsSchema(BaseModel, Generic[SortFieldT]):
    sort_by: SortFieldT | None = None
    sort_order: SortOrder = SortOrder.desc
