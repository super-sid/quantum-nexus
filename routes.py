from fastapi import FastAPI, Route, HTTPException
from fastapi.templating import Template
from .models import Post

app = FastAPI()

@app.get("/")
def read_index():
    return Template("index", {"title": "Blog"}).render()

@app.post("/create-post")
async def create_post(post: Post):
    await post.save()
    return {"message": "Post created"}

@app.get("/posts/{id}")
def read_post(id: int):
    post = Post.find_by_id(id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return Template("post", {"post": post}).render()

@app.get("/search/{query}")
async def search_posts(query: str):
    posts = Post.search(query)
    return {
        "posts": [Template("post", {"post": post}).render() for post in posts]
    }