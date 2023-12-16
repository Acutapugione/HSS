from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from .models import *

def migrate():
    # if not inspect(engine).get_table_names():
    if True:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    else:
        print("Tables on this engine already exists")