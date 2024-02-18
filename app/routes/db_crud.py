from typing import Annotated
from fastapi import APIRouter, Query, Request, Depends
from fastapi.routing import APIRoute
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from database import Session, Base, get_db, get_model
from database.models.user import User
from loguru import logger
from utils import generate_pydantic_models, schema_factory

crud_router = APIRouter()


def generate_crud_routers(pydantic_models:list)->list[SQLAlchemyCRUDRouter]:
    crud_routers = []
    
    for model in pydantic_models:
        name = model.get("name")
        base_model = model.get("base_schema")
        create_schema = model.get("create_schema")
        model = get_model(name)

        if model:
            router = SQLAlchemyCRUDRouter(
                schema=base_model,
                create_schema=create_schema,
                db_model=model,
                db=get_db,
                prefix=name,
                
            )
            crud_routers.append(router)
    return crud_routers
