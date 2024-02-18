from .base import Base
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    pwd: Mapped[str]