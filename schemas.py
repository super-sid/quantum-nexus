from fastapi import FastAPI
from fastapi.security import JWABase64Bearer
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Define a security scheme for JWT authentication
jwt_scheme = JWABase64Bearer(tokenUrl="auth:token")

# Define a template engine
templates = Jinja2Templates(directory="templates")

# Define routes
@app.get("/")
async def read_root():
    return {"message": "Welcome to the blog!"}

@app.post("/create-post")
async def create_post(content: str):
    # Create a new post object
    post = {
        "title": content,
        "body": content,
        "created_at": datetime.datetime.utcnow()
    }

    # Save the post to the database
    await models.Post.create(post)

    # Return a success message
    return {"message": "Post created successfully"}

@app.get("/search")
async def search_posts(query: str):
    # Search for posts containing the given query
    posts = await models.Post.filter(content__contains=query)

    # Return a list of matching posts
    return [post.serialize for post in posts]

@app.get("/{post_id}")
async def read_post(post_id: int):
    # Get the post with the given ID from the database
    post = await models.Post.get(post_id)

    # Return the post as a dictionary
    return post.serialize

@app.put("/{post_id}")
async def update_post(post_id: int, content: str):
    # Get the post with the given ID from the database
    post = await models.Post.get(post_id)

    # Update the post's content
    post.body = content

    # Save the updated post to the database
    await post.save()

    # Return a success message
    return {"message": "Post updated successfully"}

@app.delete("/{post_id}")
async def delete_post(post_id: int):
    # Get the post with the given ID from the database
    post = await models.Post.get(post_id)

    # Delete the post from the database
    await post.delete()

    # Return a success message
    return {"message": "Post deleted successfully"}