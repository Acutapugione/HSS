from .base import Base
from typing import List
from sqlalchemy import (
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


class Staff(Base):
    __tablename__ = "staff"
    
    name: Mapped[str] = mapped_column(String(50))
    
    service_department_id: Mapped[int] = mapped_column(ForeignKey("service_department.id"))
    service_department: Mapped["ServiceDepartment"] = relationship(back_populates="staff")
    
    access_id: Mapped[int] = mapped_column(ForeignKey("access.id"))
    access: Mapped["Access"] = relationship(back_populates="staff")

    employees: Mapped[List["Employee"]] = relationship(
        back_populates="staff",
        cascade="all, delete-orphan"
    )
    job_applications: Mapped[List["JobApplication"]] = relationship(
        back_populates="staff",
        cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"{super().__repr__()}(name={self.name!r})"
    