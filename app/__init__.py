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
from pprint import pprint
from fastapi import FastAPI, Depends, APIRouter
from typing import Annotated
from database import *
from utils import generate_pydantic_models
from sqlalchemy import select
from . routes import generate_crud_routers
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials


from database import migrate, Base


app = FastAPI(
    title="FastHealthAPI - Streamlined Healthcare Management for Ukrainian Units",
    description="""
    FastHealthAPI is a robust FastAPI-based application tailored specifically
    for the efficient management of healthcare units within Ukraine. 
    Designed to streamline operations and enhance organizational efficiency, 
    this API empowers users to handle various aspects crucial to healthcare management.
    """,
    version="0.0.1",
)

db_crud_router = APIRouter()

pydantic_models = generate_pydantic_models(
    Base.metadata,
    "Base",
    base_model_exclude_columns=["id",],
    exclude_tables=[
        "user",
    ]
)
for router in generate_crud_routers(pydantic_models):
    db_crud_router.include_router(router)

app.include_router(db_crud_router)

security = HTTPBasic()


@app.get(
    "/users/me/"
)
def read_curr_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)],  db: Session = Depends(get_db)):
    user = db.query(User).where(User.username == credentials.username,
                                User.pwd == credentials.password).first()
    if user:
        return {
            "status": True,
            "username": credentials.username,
            "password": credentials.password
        }
    return {
        "status": False
    }


# pprint(globals())
