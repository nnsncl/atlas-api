import os
from dotenv import load_dotenv

from jose import JWTError, jwt
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.orm.session import Session
from . import schemas, database, models

# Env variables
load_dotenv()
OAUTH_SECRET_KEY = os.environ.get('OAUTH_SECRET_KEY')
OAUTH_ALGORITHM = os.environ.get('OAUTH_ALGORITHM')
ACCESS_TOKEN_TTL_MINS = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    encode_input = data.copy()

    expire_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_TTL_MINS)
    encode_input.update({"exp": expire_at})

    encoded_jwt = jwt.encode(
        encode_input, OAUTH_SECRET_KEY, algorithm=OAUTH_ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(
            token, OAUTH_SECRET_KEY,
            algorithms=[OAUTH_ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credential_exception

    return token_data


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
