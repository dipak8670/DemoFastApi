from unittest import mock
from luffy.api.src.main import app
from fastapi.testclient import TestClient
from fastapi import status

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


@mock.patch("luffy.api.src.main.DynamoDbExecutor")
def test_add_success(mock_db_client):
    mock_db_client_instance = mock_db_client.return_value
    mock_db_client_instance.save.return_value = {"status": "success"}
    request_data = {"name": "John", "phone": "1234567890"}
    response = client.post("/add", json=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hi, John! Your phone number is 1234567890."}


def test_add_missing_params():
    request_data = {"name": "John"}
    response = client.post("/add", json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": "Parameters name and/or phone are missing."}
