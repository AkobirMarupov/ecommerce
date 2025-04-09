from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/ecommerce"

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
