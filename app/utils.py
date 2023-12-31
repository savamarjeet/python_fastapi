from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from .const import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY
from fastapi import Query
from app.database import SessionLocal
from app import models

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_token_from_db(user_id: int):
    session = SessionLocal()
    return session.query(models.TokenTable).filter(models.TokenTable.user_id == user_id).first()

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

 
def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
     
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_pagination_params(
    skip: int = Query(0, title="Skip the first N items", ge=0),
    limit: int = Query(5, title="Limit the number of items to retrieve", le=20),
):
    return {"skip": skip, "limit": limit}
