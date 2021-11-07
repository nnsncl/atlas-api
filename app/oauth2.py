import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Env variables
load_dotenv()
OAUTH_SECRET_KEY = os.environ.get('OAUTH_SECRET_KEY')
OAUTH_ALGORITHM = os.environ.get('OAUTH_ALGORITHM')
ACCESS_TOKEN_TTL_MINS = 30


def create_access_token(data: dict):
    encode_input = data.copy()

    expire_at = str(datetime.now() + timedelta(minutes=ACCESS_TOKEN_TTL_MINS))
    encode_input.update({"expire_at": expire_at})

    encoded_jwt = jwt.encode(
        encode_input, OAUTH_SECRET_KEY, algorithm=OAUTH_ALGORITHM)

    return encoded_jwt
