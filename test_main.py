# test_main.py

from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app instance

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
