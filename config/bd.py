import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

env_file = os.getenv("APP_ENV") or ".env"
if env_file != ".env":
    load_dotenv(env_file, override=True)
else:
    load_dotenv()

_DB_HOST=os.getenv('DB_HOST')
_DB_USER=os.getenv('DB_USER')
_DB_PASSWORD=os.getenv('DB_PASSWORD')
_DB_PORT=os.getenv('DB_PORT')
_DB_NAME=os.getenv('DB_NAME')


connection = f"mysql+pymysql://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}"
engine = create_engine(connection, pool_pre_ping=True)
SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)
Base = declarative_base()


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()