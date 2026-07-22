from app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class HealthTable(Base):
    __tablename__ = "health"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String)
