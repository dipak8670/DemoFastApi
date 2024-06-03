from luffy.api.src.main import app
from fastapi.testclient import TestClient
from fastapi import status

from luffy.api.src.common.models.name_request import NameRequest

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, FastAPI!"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_hi():
    response = client.get("/hi")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hi, Dipak!"}
    
def test_add_success():
        request_data = {"name": "John", "phone": "1234567890"}
        response = client.post("/add", json=request_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Hi, John! Your phone number is 1234567890."}
        
def test_add_missing_params():
        request_data = {"name": "John"}
        response = client.post("/add", json=request_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {"detail": "Parameters name and/or phone are missing."}
