import time

import os
from dotenv import load_dotenv

from fastapi import FastAPI

import psycopg2
from psycopg2.extras import RealDictCursor

from .database import engine
from .routes import post, user, auth
from . import models


# Env variables
load_dotenv()
HOST_URL = os.environ.get('HOST_URL')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# App variables
APP_TITLE = 'Atlas API'
APP_DESC = 'This API exists to gather data of any kind from diverse sources.'
APP_VERSION = '1.0.0'
APP_SERVERS = [{"url": HOST_URL, "description": "Development Server"}]

models.Base.metadata.create_all(bind=engine)

# Init FastAPI app
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESC,
    version=APP_VERSION,
    servers=APP_SERVERS)

# Connect to database
while True:
    # Loop over the connection until it's on,
    # otherwise run this code again every 2 seconds.
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print('Connected to Atlas 🌍')
        break
    except Exception as error:
        print('Connection to Atlas failed.')
        print('message', error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to Atlas 🌍"}
