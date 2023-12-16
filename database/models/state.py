from .base import Base
from typing import List
from sqlalchemy import String, Column
from sqlalchemy.sql.schema import ScalarElementColumnDefault
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

# Column.server_default
class State(Base):
    __tablename__ = "state"
    
    name: Mapped[str] = mapped_column(String(50))
    
    job_applications: Mapped[List["JobApplication"]] = relationship(
        back_populates="state",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"{super().__repr__()}(name={self.name!r})"
    