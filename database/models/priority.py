from .base import Base
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


class Priority(Base):
    __tablename__ = "priority"
    
    level: Mapped[int]
    name: Mapped[str] = mapped_column(String(50))
    
    job_applications: Mapped[List["JobApplication"]] = relationship(
        back_populates="priority",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"{super().__repr__()}(name={self.name!r})"
    