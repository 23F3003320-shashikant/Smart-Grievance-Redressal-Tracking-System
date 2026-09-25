from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/database_name"
engine = create_engine(DATABASE_URL)
