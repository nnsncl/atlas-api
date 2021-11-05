from typing import Optional
from fastapi import FastAPI, Response, status
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


def find_post(id):
    for post in stored_posts:
        if post['id'] == id:
            return post


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


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    filtered_post = find_post(id)
    if not filtered_post:
        response.status_code = status.HTTP_404_NOT_FOUND

    return {"data": filtered_post}


@app.delete('posts/{id}')
def delete_post(id: int):
    post_to_delete = find_post(id)
    return {f"Post {post_to_delete} has been deleted."}

