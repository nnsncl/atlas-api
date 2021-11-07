from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostReponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
