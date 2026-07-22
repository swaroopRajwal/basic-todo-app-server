from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    status: bool
    data: T


class PaginatedResponseSchema(BaseModel, Generic[T]):
    status: bool
    data: list[T]
    page: int
    limit: int
    count: int
