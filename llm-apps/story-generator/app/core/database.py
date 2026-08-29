from sqlmodel import create_engine, Session, SQLModel

from app.core.config import settings


DATABASE_URL = settings.database_url

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
    
def get_session():
    with Session(engine) as session:
        yield session



   
 