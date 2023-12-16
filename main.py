from database import migrate, Base
from uvicorn import run
from utils import generate_pydantic_models
from app import app


migrate()


if __name__ == "__main__":
    # pydantic_models = generate_pydantic_models(Base.metadata, "Base")
    # for key, val in pydantic_models.items():
    #     globals()[key]=val
    # print(globals().get('Access'))
    
    
    run("main:app", reload=True)