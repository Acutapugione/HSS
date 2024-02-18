from fastapi import APIRouter
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from database import get_db, get_model
from database.models.user import User
from loguru import logger


crud_router = APIRouter()

@logger.catch
def generate_crud_routers(pydantic_models:list)->list[SQLAlchemyCRUDRouter]:
    crud_routers = []
    
    for model in pydantic_models:
        name = model.get("name")
        base_schema = model.get("base_schema")
        create_schema = model.get("create_schema")
        model = get_model(name)

        if model:
            router = SQLAlchemyCRUDRouter(
                schema=base_schema,
                create_schema=create_schema,
                db_model=model,
                db=get_db,
                prefix=name,
                
            )
            crud_routers.append(router)
    return crud_routers
