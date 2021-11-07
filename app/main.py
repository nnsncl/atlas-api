import time
from typing import List

import os
from dotenv import load_dotenv

from fastapi import FastAPI, Response, status, HTTPException, Depends

import psycopg2
from psycopg2.extras import RealDictCursor

from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models, schemas


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


# Methods
@app.get("/", response_model=List[schemas.PostReponse])
def root():
    return {"message": "Welcome to Atlas 🌍"}


@app.get("/posts")
# Get all items
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReponse)
# Create an item
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Unpack post fields dictionnary to map every inputs provided by the model.
    created_post = models.Post(**post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    return created_post


@app.get("/posts/{id}", response_model=schemas.PostReponse)
# Get a single item by ID
def get_post(id: int, db: Session = Depends(get_db)):
    filtered_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not filtered_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")

    return filtered_post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# Delete an item by ID
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostReponse)
# Update an item by ID
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    filtered_post = query.first()

    if filtered_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")

    query.update(post.dict(), synchronize_session=False)
    db.commit()

    return query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
# Create a new user
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)

    return created_user
