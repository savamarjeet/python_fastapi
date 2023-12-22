from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .const import DATABASE_URI

# create a sqlite engine instance
engine = create_engine(DATABASE_URI)

# create declarative base meta instance
Base = declarative_base()

# create session local class for session maker
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
