from .base import Base
from sqlalchemy import (
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


class JobApplication(Base):
    __tablename__ = "job_application"
    
    text: Mapped[str] = mapped_column(String(350))
    
    service_department_id: Mapped[int] = mapped_column(ForeignKey("service_department.id"))
    service_department: Mapped["ServiceDepartment"] = relationship(back_populates="job_applications")
    
    state_id: Mapped[int] = mapped_column(ForeignKey("state.id"))
    state: Mapped["State"] = relationship(back_populates="job_applications")
    
    priority_id: Mapped[int] = mapped_column(ForeignKey("priority.id"))
    priority: Mapped["Priority"] = relationship(back_populates="job_applications")

    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    employee: Mapped["Employee"] = relationship(back_populates="job_applications")

    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.id"))
    staff: Mapped["Staff"] = relationship(back_populates="job_applications")


    def __repr__(self) -> str:
        return f"{super().__repr__()}(text={self.text!r})"
