# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:karachi.90@localhost/hospital_db"



# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

# SessionLocal = sessionmaker(
#     autocommit=True,
#     autoflush=True,
#     bind=engine)

# Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:karachi.90@localhost/hospital_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()