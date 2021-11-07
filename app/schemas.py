from os import access
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    # Post base schema
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    # Post creation schema
    # Extends PostBase schema
    pass


class PostReponse(PostBase):
    # Post creation output schema
    id: int
    created_at: datetime

    class Config:
        # Convert SQLAlchemy query to dict
        orm_mode = True


class UserCreate(BaseModel):
    # User creation schema
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    # User creation output schema
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        # Convert SQLAlchemy query to dict
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
    