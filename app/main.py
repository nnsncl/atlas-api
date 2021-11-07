from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os

# Env variables
load_dotenv()
host_url = os.environ.get('HOST_URL')
db_name = os.environ.get('DB_NAME')
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

# Init FastAPI app
app = FastAPI(
    title="Atlas API",
    description="This API was built with FastAPI and exists to gather data of any kind from diverse sources.",
    version="1.0.0",
    servers=[{
        "url": host_url,
        "description": "Development Server"
    }])


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Loop over the connection until it's on,
# otherwise run this code again every 2 seconds.
while True:
    try:
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print('Connected to Atlas 🌍')
        break
    except Exception as error:
        print('Connection to Atlas failed.')
        print('message', error)
        time.sleep(2)


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


def find_post_index(id):
    for index, post in enumerate(stored_posts):
        if post['id'] == id:
            return index


@app.get("/")
def root():
    return {"message": "Atlas API"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Use %s to sanitize inputs and avoid SQL injections.
    # Values are provided as the second paramter of the cursor.execute method.
    cursor.execute("""
        INSERT INTO posts (title, content, published)
        VALUES (%s, %s, %s)
        RETURNING *
    """, (
        post.title,
        post.content,
        post.published,
    ))
    created_post = cursor.fetchone()
    return {"data": created_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    filtered_post = find_post(id)
    if not filtered_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")
    return {"data": filtered_post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_post_index(id)
    if post_index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")

    stored_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = find_post_index(id)
    if post_index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")

    post_dict = post.dict()
    post_dict['id'] = id
    stored_posts[post_index] = post_dict
    return {"data": post_dict}
