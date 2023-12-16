from .base import Base
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


class ServiceDepartment(Base):
    __tablename__ = "service_department"
    
    name: Mapped[str] = mapped_column(String(50))
    
    job_applications: Mapped[List["JobApplication"]] = relationship(
        back_populates="service_department",
        cascade="all, delete-orphan"
    )
    
    staff: Mapped["Staff"] = relationship(back_populates="service_department")
    
    def __repr__(self) -> str:
        return f"{super().__repr__()}(name={self.name!r})"
    