from pydantic import BaseModel, Field, create_model
from sqlalchemy import MetaData
from loguru import logger
from typing import Callable, Type, TypeVar
from typing import Dict, List, Optional, Tuple


T = TypeVar("T", bound=BaseModel)

def schema_factory(
    schema_cls: Type[T], pk_field_name: str = "id", name: str = "Create"
) -> Type[T]:
    """
    Is used to create a CreateSchema which does not contain pk
    """

    fields = {
        name: (f.annotation, ...)
        for name, f in schema_cls.model_fields.items()
        if name != pk_field_name
    }

    name = schema_cls.__name__ + name
    schema: Type[T] = create_model(__model_name=name, **fields)  # type: ignore
    return schema


def generate_model(
    name: str,
    inheritanced: Tuple[type] = [],
    fields: Dict[str, type] = {},
    inner_classes: List[type] = [],
) -> type:
    model_fields = fields.copy()
    model = type(name, inheritanced, {})
    for field, type_ in model_fields.items():
        setattr(model, field, Field())
    for inner_cls in inner_classes:
        setattr(model, inner_cls.__name__, inner_cls)
    model.__annotations__ = model_fields

    return model


@logger.catch
def generate_pydantic_models(
    meta: MetaData,
    create_postfix: str = "Create",
    full_postfix: str = "Full",
    base_model_exclude_columns: List[str] = [
        "id",
    ],
    exclude_tables: List[str] = [],
) -> List[Type]:
    "Function to generate Pydantic models from SQLAlchemy metadata"
    pydantic_models = []

    for name, model in meta.tables.items():

        if model in exclude_tables or name in exclude_tables:
            continue
        cls_name = "".join([n.title() for n in name.split("_")])
        pydantic_model = {"name": str(cls_name)}
        # parse columns in Base model
        columns = list(
            filter(
                lambda col: col.name not in base_model_exclude_columns, model.columns
            )
        )

        create_annotations = {}
        for column in model.columns:
            create_annotations[column.name] = column.type.python_type

        model_annotations = {}
        for column in columns:
            model_annotations[column.name] = column.type.python_type

        inner_cls = type("Config", (), {})
        inner_cls.orm_mode = True
        

        base = generate_model(
            name=f"{cls_name}Base",
            inheritanced=(BaseModel,),
            fields=create_annotations,
        )
        model_create = generate_model(
            name=f"{cls_name}{create_postfix}",
            inheritanced=(base,),
            fields=create_annotations,
        )

        model_base = generate_model(
            name=f"{cls_name}{full_postfix}",
            inheritanced=(model_create,),
            fields=model_annotations,
            inner_classes=[
                inner_cls,
            ],
        )
        # pydantic_model["base"] = base
        pydantic_model["base_schema"] = schema_factory(model_base)
        pydantic_model["create_schema"] = schema_factory(model_create)
        pydantic_models.append(pydantic_model)

    return pydantic_models
