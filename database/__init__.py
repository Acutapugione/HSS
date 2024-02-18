from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})

Session = sessionmaker(engine)

from .models import *

def migrate():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
migrate()

# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
        
def get_model(name):
    
    if name in globals():
        if issubclass(globals().get(name), Base):
            return globals().get(name)