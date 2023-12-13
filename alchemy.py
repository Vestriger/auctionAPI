from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost/auction"
engine = create_engine(DATABASE_URL, echo=True)
session_factory = sessionmaker(engine)