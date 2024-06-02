from fastapi import FastAPI, HTTPException
from typing import Optional


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


@app.post("/nam")
def putName(name: Optional[str] = None):
    if name:
        return {"message": f"Hi, {name}!"}
    else:
        raise HTTPException(status_code=422, detail="Name parameter is missing.")
