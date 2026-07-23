from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TodoBase(BaseModel):
    title: str = Field(max_length=150, min_length=1)
    description: str | None = Field(default=None, max_length=1000)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=150, min_length=1)
    description: str | None = Field(default=None, max_length=1000)
    is_completed: bool | None = None


# Schema for returning a Todo from the API (includes DB-generated fields)
class TodoResponse(TodoBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_completed: bool = False

    # Pydantic V2 config to allow reading from SQLAlchemy ORM objects
    model_config = ConfigDict(from_attributes=True)
