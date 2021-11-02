from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Atlas API"}


@app.get("/posts")
def get_posts():
    return {"message": "Post data"}
