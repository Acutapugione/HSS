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


class Message(Base):
    __tablename__ = "message"
    text: Mapped[str] = mapped_column(String(350))
    telergam_id: Mapped[str]
    is_sended: Mapped[bool] = mapped_column(default=False)
    is_confirmed: Mapped[bool] = mapped_column(default=False)
