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
    # index: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=None, nullable=True)
    # id: Mapped[int] = mapped_column(nullable=True, default=None)
    text: Mapped[str] = mapped_column(String(350))
    telegram_id: Mapped[str]
    phone_number: Mapped[str]
    is_sended: Mapped[bool] = mapped_column(default=False)
    is_confirmed: Mapped[bool] = mapped_column(default=False)
