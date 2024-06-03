from fastapi import FastAPI, HTTPException

from luffy.api.src.common.models.request_model import RequestModel
from luffy.api.src.common.utils.dynamoDb_executor import DynamoDbExecutor


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

@app.post("/add")
def add(request: RequestModel):
    if request.name and request.phone:
        item={}
        item["name"]=request.name
        item["phone"]=request.phone
        try:
            dynamoDb_executor = DynamoDbExecutor()
            dynamoDb_executor.save(item)
            return {"message": f"Hi, {request.name}! Your phone number is {request.phone}."}
        except Exception as e:
            raise HTTPException(status_code=422, detail=e)
        
    else:
        raise HTTPException(status_code=422, detail="Parameters name and/or phone are missing.")

