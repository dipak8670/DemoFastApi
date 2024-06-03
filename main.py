from fastapi import FastAPI, HTTPException
from typing import Optional

from models import NameRequest


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/hi")
async def hi():
    return {"message": "Hi, Dipak!"}


@app.post("/name")
def putName(request: NameRequest):
    if request.name:
        return {"message": f"Hi, {request.name}!"}
    else:
        raise HTTPException(status_code=422, detail="Name parameter is missing.")
