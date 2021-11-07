from typing import List
from .. import models, schemas
from ..database import get_db

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/posts", response_model=List[schemas.PostReponse])
# Get all items
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReponse)
# Create an item
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Unpack post fields dictionnary to map every inputs provided by the model.
    created_post = models.Post(**post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    return created_post


@router.get("/posts/{id}", response_model=schemas.PostReponse)
# Get a single item by ID
def get_post(id: int, db: Session = Depends(get_db)):
    filtered_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not filtered_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with an id of {id} wasn't found.")

    return filtered_post


@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/posts/{id}", response_model=schemas.PostReponse)
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
