from .base import Base
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


class Employee(Base):
    __tablename__ = "employee"
    
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[int] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    telergam_id: Mapped[str] = mapped_column(unique=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_interim: Mapped[bool] = mapped_column(default=False)

    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.id"))
    staff: Mapped["Staff"] = relationship(back_populates="employees")

    # staff_extra_id: Mapped[int] = mapped_column(ForeignKey("staff.id"))
    # staff_extra: Mapped["Staff"] = relationship(back_populates="employees")

    job_applications: Mapped[List["JobApplication"]] = relationship(
        back_populates="employee",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"{super().__repr__()}(first_name={self.first_name!r}, surname={self.surname!r}, last_name={self.last_name!r})"