import time
from random import randrange

import os
from dotenv import load_dotenv

from fastapi import FastAPI, Response, status, HTTPException, Depends

import psycopg2
from psycopg2.extras import RealDictCursor

from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models


# Env variables
load_dotenv()
host_url = os.environ.get('HOST_URL')
db_name = os.environ.get('DB_NAME')
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

# App variables
app_title = 'Atlas API'
app_description = 'This API exists to gather data of any kind from diverse sources.'
app_version = '1.0.0'
app_servers = [{"url": host_url, "description": "Development Server"}]

models.Base.metadata.create_all(bind=engine)

# Init FastAPI app
app = FastAPI(
    title=app_title,
    description=app_description,
    version=app_version,
    servers=app_servers)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Connect to database
while True:
    # Loop over the connection until it's on,
    # otherwise run this code again every 2 seconds.
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


@app.get("/")
def root():
    return {"message": "Welcome to Atlas 🌍"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # Unpack post fields dictionnary to map every inputs provided by the model.
    created_post = models.Post(**post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    return {"data": created_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    filtered_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not filtered_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")

    return {"data": filtered_post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    filtered_post = query.first()

    if filtered_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")

    query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"data": query.first()}
