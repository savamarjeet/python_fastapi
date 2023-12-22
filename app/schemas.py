from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=60)
    email: EmailStr
    
class UserDetail(UserBase):
    address: Optional[str] = None
    created_at: datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=60)
    email: EmailStr
    password: str
    address: Optional[str] = None

class Requestdetails(BaseModel):
    email: EmailStr
    password: str
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_at: datetime

class Post(BaseModel):
    title: str = Field(..., min_length=5, max_length=60)
    content: str = Field(..., min_length=10, max_length=256)

class DetailPost(Post):
    author: UserBase
    id: int
    created_at: datetime

class AuthorPost(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    is_active: bool
