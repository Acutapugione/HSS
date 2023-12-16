"""
Title: FastHealthAPI - Streamlined Healthcare Management for Ukrainian Units

Description:
FastHealthAPI is a robust FastAPI-based application tailored specifically for the efficient management of healthcare units within Ukraine. Designed to streamline operations and enhance organizational efficiency, this API empowers users to handle various aspects crucial to healthcare management.

Key Features:

Staff Management: Easily manage and oversee staff details, including their roles, schedules, contact information, and qualifications. This feature enables seamless staff administration, allowing for the efficient allocation of resources within healthcare units.

Employee Database: A comprehensive employee database system assists in storing and organizing essential employee information. Users can track performance, manage certifications, and facilitate HR-related tasks seamlessly.

Service Departments: This API enables the creation, modification, and monitoring of service departments within healthcare units. Administrators can efficiently organize, assign, and oversee different departments to ensure smooth operations.

Job Application Management: The API provides a structured framework for managing job applications within healthcare units. This includes the ability to post job openings, accept applications, review candidate details, and manage the hiring process efficiently.

Use Cases:

Staff Allocation: Healthcare unit managers can efficiently assign staff to specific departments based on their expertise and availability, optimizing the operational workflow.

Employee Record Keeping: HR departments can easily access and update employee records, certifications, and performance data, streamlining administrative tasks.

Departmental Organization: Administrators can create, modify, and manage service departments to ensure proper functionality and efficient allocation of resources.

Job Application Tracking: Human resources personnel can oversee the entire job application process, from posting job openings to reviewing applications, and managing the hiring process.

FastHealthAPI is an invaluable tool for healthcare unit administrators and managers seeking a reliable, secure, and efficient system for managing staff, employees, service departments, and job applications within the Ukrainian healthcare sector. Built on the FastAPI framework, it offers a powerful and scalable solution to optimize healthcare operations.
"""
from fastapi import FastAPI, Depends
from database import  *
from utils import generate_pydantic_models
from sqlalchemy import select
from sqlalchemy.orm import Session
import logging


app = FastAPI(
    title="FastHealthAPI - Streamlined Healthcare Management for Ukrainian Units",
    description="""
    FastHealthAPI is a robust FastAPI-based application tailored specifically
    for the efficient management of healthcare units within Ukraine. 
    Designed to streamline operations and enhance organizational efficiency, 
    this API empowers users to handle various aspects crucial to healthcare management.
    """,
    version="0.0.1"
    )
def my_function(x, y):
    """
    This function calculates the sum and difference of two numbers.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        tuple: A tuple containing the sum and difference of x and y.

    Examples:

    ```
    >>> my_function(15, 3)  # Output: (8, 2)
    >>> my_function(-2, 1254)  # Output: (2, -6)
    ```
    """
    ...

# Dependency
def get_db():
    """
    docs
    ```python
    get_db()
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# from pydantic import BaseModel
# from .. import app

# class Access(BaseModel):
#     item_id:int

# @app.put("/access/{item_id}")
# def update_item(item_id: int, item: Access):
#     return {"name": item.name, "item_id": item_id}

pydantic_models = generate_pydantic_models(Base.metadata, "Base")
for model in pydantic_models:
    name = model.get('name')
    base_schema = model.get('base')
    create_schema = model.get('create')
    main_schema = model.get('full')
    db_class = model.get('db_class')
    
    @app.post(path=f'/{name}/create', response_model=main_schema)
    def create_item(item: create_schema, db: Session = Depends(get_db)):
        try:
            new_item = globals().get(name)(**item.dict())
            logging.info(new_item)
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
        except Exception as e:
            db.rollback()
            logging.exception(msg=str(e))
        return item
            
    @app.get(path=f'/{name}/items', response_model=list[main_schema])
    def get_items(db: Session = Depends(get_db)):
        return db.query(db_class).all()

    @app.get(path=f'/{name}/'+'{id}', response_model=main_schema)
    def get_item(id: int, db: Session = Depends(get_db)):
        return db.query(db_class).first()

        
    # @app.put(path=f'/{name}/'+'{id}', response_model=main_schema)
    # def update_item(id: int, item: create_schema, db: Session = Depends(get_db)):
    #     with Session(engine) as session:
    #         obj = session.scalars(select(db_class)).one()
    #         if obj:
    #             obj
    #         return item