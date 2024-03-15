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

from fastapi import (
    FastAPI,
    Depends,
    APIRouter,
    Request,
    HTTPException,
    status,
)

from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from sqlalchemy.orm import Session
from typing import Annotated
from loguru import logger


from database import Base, get_db, User
from utils import generate_pydantic_models
from .routes import generate_crud_routers, appeals_router


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
    base_model_exclude_columns=[
        "id",
    ],
    exclude_tables=[
        "user",
    ],
)
for router in generate_crud_routers(pydantic_models):
    db_crud_router.include_router(router)



security = HTTPBasic()

def get_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)], db: Session = Depends(get_db),):
    user = (
        db.query(User)
        .where(User.username == credentials.username)
        .first()
    )
    if user:
        current_password_bytes = credentials.password.encode("utf8")
        correct_password_bytes = user.pwd.encode("utf8")
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )
        if is_correct_password:
            return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get("/users/me/")
def read_curr_user(
    status: Annotated[bool, Depends(get_user)]
):
    return status
app.include_router(appeals_router)
app.include_router(db_crud_router)





PATH_LIST = [x.path for x in app.routes]


@app.middleware("http")
async def add_wrong_request_path_redirect(request: Request, call_next):
    print(request.headers)
    url = request.url.path
    if url in PATH_LIST:
        response = await call_next(request)
        logger.info(
            f"{request.client} : {request.url} -> {response.status_code}")
    else:
        response = RedirectResponse(PATH_LIST[-1])
    return response
