from fastapi import FastAPI, Security, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello, World!": "From utils.py"}

@app.post("/login")
async def login(username: str, password: str):
    # Implement authentication logic here
    return {"logged_in": True}

@app.get("/protected")
async def protected(token: str = Depends()):
    # Check if token is valid
    return {"protected_content": "From utils.py"}