import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.models import Base

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing or could not be loaded from .env")

#session for raw sql
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

#Creates ORM session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Yield an ORM Session instead of a raw Connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()