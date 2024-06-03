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


def test_putName_with_name():
    response = client.post("/name", json={"name": "Alice"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hi, Alice!"}


def test_putName_without_name():
    response = client.post("/name", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": "Name parameter is missing."}
