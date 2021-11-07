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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to Atlas 🌍"}