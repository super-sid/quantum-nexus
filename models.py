from fastapi import FastAPI, Model
from typing import List

class Post(Model):
    id = FastAPI.UUID()
    title = String(required=True)
    content = String(required=True)
    author = Reference("User", fields=["id"])

class User(Model):
    id = FastAPI.UUID()
    name = String(required=True)
    email = Email(required=True)

class SearchResult(Model):
    id = FastAPI.UUID()
    title = String
    content = String
    author = Reference("User", fields=["id"])

app = FastAPI()

@app.get("/users")
async def read_users():
    users = User.query.all()
    return {user.id: user.name for user in users}

@app.post("/users/<int:user_id>")
async def create_user(user_id: int):
    user = User(name=request.json["name"], email=request.json["email"])
    await user.save()
    return {"message": "User created"}

@app.get("/posts")
async def read_posts():
    posts = Post.query.all()
    return {post.id: post.title for post in posts}

@app.post("/posts/<int:post_id>")
async def create_post(post_id: int):
    post = Post(title=request.json["title"], content=request.json["content"])
    await post.save()
    return {"message": "Post created"}

@app.get("/search/<str:query>")
async def search_posts(query: str):
    posts = Post.query.filter(Post.title.contains(query)).all()
    return {post.id: post.title for post in posts}