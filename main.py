from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

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
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10e9)

    stored_posts.append(post_dict)
    return {"data": post_dict}

# In "/posts/{id}", {id} is the Path Parameter
@app.get("/posts/{id}")
def get_post(id: int):
    return {"post_detail": f"Here is post {id}"}