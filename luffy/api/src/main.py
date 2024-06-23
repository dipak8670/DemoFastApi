from fastapi import FastAPI, HTTPException

from luffy.api.src.common.models.request_model import RequestModel
from luffy.api.src.common.utils.dynamoDb_executor import DynamoDbExecutor
import logging

app = FastAPI()


@app.get("/")
async def root():
    logging.info("Hello, Students!")
    return {"message": "Hello, Students!"}


@app.get("/health")
async def health_check():
    logging.info("Health check successful.")
    return {"status": "ok"}


@app.post("/add_student")
def add_student(request: RequestModel):
    if request.name and request.roleNumber:
        item = {}
        item["name"] = request.name
        item["role_number"] = request.roleNumber
        try:
            dynamoDb_executor = DynamoDbExecutor()
            dynamoDb_executor.save(item)
            logging.info(f"Student {request.name} added successfully.")
            return {
                "message": f"Hi, {request.name}! Your role number is {request.roleNumber}."
            }
        except Exception as e:
            logging.error(f"Error adding student: {e}")
            raise HTTPException(status_code=422, detail=e)

    else:
        logging.error(
            f"Parameters name and/or role number are missing in the request.{request}"
        )
        raise HTTPException(
            status_code=422, detail="Parameters name and/or role number are missing."
        )
