from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


stored_posts = [
    {
        "title": "Some title",
        "content": "Some content",
        "id": 1
    },
    {
        "title": "Some other title",
        "content": "Some other content",
        "id": 2
    },
]


@app.get("/")
def root():
    return {"message": "Atlas API"}


@app.get("/posts")
def get_posts():
    return {"data": stored_posts}


@app.post("/posts")
def create_post(post: Post):
    print(post.dict())
    return {"data": post}
