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


class Access(Base):
    __tablename__ = "access"
    
    name: Mapped[str] = mapped_column(String(50))
    
    super_admin: Mapped[bool] = mapped_column(default=False)
    
    app_user_allowed: Mapped[bool] = mapped_column(default=False)
    
    get_staff_allowed: Mapped[bool] = mapped_column(default=False)
    edit_staff_allowed: Mapped[bool] = mapped_column(default=False)
    
    get_job_application_allowed: Mapped[bool] = mapped_column(default=False)
    edit_job_application_allowed: Mapped[bool] = mapped_column(default=False)
    
    get_employee_allowed: Mapped[bool] = mapped_column(default=False)
    edit_employee_allowed: Mapped[bool] = mapped_column(default=False)
    
    get_employee_allowed: Mapped[bool] = mapped_column(default=False)
    edit_employee_allowed: Mapped[bool] = mapped_column(default=False)
    
    get_service_department_allowed: Mapped[bool] = mapped_column(default=False)
    edit_service_department_allowed: Mapped[bool] = mapped_column(default=False)
    
    
    staff: Mapped["Staff"] = relationship(back_populates="access")
    
    def __repr__(self) -> str:
        return f"{super().__repr__()}(name={self.name!r})"
    