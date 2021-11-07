from .. import models, schemas, utils
from ..database import get_db

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
# Create a new user
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash user password and update user.password before the payload is submit.
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)

    return created_user


@router.get('/{id}', response_model=schemas.UserOutput)
def get_user(id: int,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with an id of {id} wasn't found.")

    return user
