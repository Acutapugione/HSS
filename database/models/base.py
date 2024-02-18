from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True) # noqa

    # @classmethod
    # @property
    # def __tablename__(self) -> str:
    #     return f"{self.__class__.__name__.lower()}s"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"