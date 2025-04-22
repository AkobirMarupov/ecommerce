from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql+psycopg2://postgres:akobir2004@localhost/online_market"

engine = create_engine(DATABASE_URL, echo= True)

SessionLocal = sessionmaker(bind= engine)

Base = declarative_base()

