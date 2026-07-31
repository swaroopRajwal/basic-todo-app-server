from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, String, Table, Column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base

if TYPE_CHECKING:
    from app.database.models.todo import TodoTable


todo_tags = Table(
    "todo_tags",
    Base.metadata,
    Column("todo_id", String, ForeignKey("todos.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", String, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class TagsTable(Base):
    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    __table_args__ = (Index("uq_tags_name_lower", func.lower(name), unique=True),)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    todos: Mapped[list["TodoTable"]] = relationship(
        secondary=todo_tags,
        back_populates="tags",
        default_factory=list,
    )
