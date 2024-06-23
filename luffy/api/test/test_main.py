from unittest import mock
from luffy.api.src.main import app
from fastapi.testclient import TestClient
from fastapi import status

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, Students!"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


@mock.patch("luffy.api.src.main.DynamoDbExecutor")
def test_add_success(mock_db_client):
    mock_db_client_instance = mock_db_client.return_value
    mock_db_client_instance.save.return_value = {"status": "success"}
    request_data = {"name": "John", "roleNumber": "1234567890"}
    response = client.post("/add_student", json=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hi, John! Your role number is 1234567890."}


def test_add_missing_params():
    request_data = {"name": "John"}
    response = client.post("/add_student", json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": "Parameters name and/or role number are missing."
    }
