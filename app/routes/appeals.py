from typing import Dict
from fastapi import APIRouter, Depends
from database import Session, get_db, get_model
from database.models import Message, Employee
from sqlalchemy import select
from loguru import logger


appeals_router = APIRouter()


@appeals_router.put("/mark_as_read_appeal")
def mark_as_read_appeal(q: Dict, db: Session = Depends(get_db)): 
    print(f"{q=}")
    with db as _:
        print(f"{q=}")
        appeal:Message = _.scalars(
            select(Message).where(
                Message.text == q.get("text"), 
                Message.telegram_id == q.get("telegram_id"),
                Message.is_sended == False,
            )
        ).first()
        print(f"{appeal=}")
        if appeal:
            print(f"{appeal.is_sended=}")
            appeal.is_sended = True
            _.add(appeal)
            _.commit()
            print(f"{appeal.is_sended=}")

            return appeal.id
    return {"error": "not found"}