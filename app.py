from fastapi import FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Template
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from typing import Optional

app = FastAPI()

# Define a route for the home page
@app.get("/")
async def read_root():
    return {"message": "Welcome to my blog"}

# Define a route for creating a new post
@app.post("/posts/")
async def create_post(content: str = Depends()):
    # Validate the content
    if not content:
        raise ValueError("Content cannot be empty")
    
    # Create a new post object
    post = {
        "title": content,
        "author": "Anonymous",
        "created_at": datetime.datetime.utcnow()
    }
    
    # Save the post to the database
    db = get_db()
    await db.insert("posts", post)
    
    # Return a success message
    return JSONResponse(content="Post created successfully!", status_code=201)

# Define a route for reading a specific post
@app.get("/posts/{id}")
async def read_post(id: int = Depends()):
    # Get the post from the database
    db = get_db()
    post = await db.get("posts", id)
    
    # Return the post as a JSON response
    return JSONResponse(content=post, status_code=200)

# Define a route for updating a post
@app.put("/posts/{id}")
async def update_post(id: int, content: str = Depents()):
    # Get the post from the database
    db = get_db()
    post = await db.get("posts", id)
    
    # Validate the content
    if not content:
        raise ValueError("Content cannot be empty")
    
    # Update the post in the database
    post["content"] = content
    await db.update("posts", post, id)
    
    # Return a success message
    return JSONResponse(content="Post updated successfully!", status_code=200)

# Define a route for deleting a post
@app.delete("/posts/{id}")
async def delete_post(id: int):
    # Get the post from the database
    db = get_db()
    post = await db.get("posts", id)
    
    # Delete the post from the database
    await db.delete("posts", id)
    
    # Return a success message
    return JSONResponse(content="Post deleted successfully!", status_code=204)