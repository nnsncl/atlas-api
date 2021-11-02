from fastapi import FastAPI
from fastapi import Body

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Atlas API"}


@app.get("/posts")
def get_posts():
    return {"message": "Post data"}


@app.post("/create")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"nex_post": f"title: {payload['title']} content: {payload['content']}"}
