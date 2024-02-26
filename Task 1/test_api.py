import pytest
from fastapi.testclient import TestClient
from main import app  # assuming your FastAPI app is named 'app' in main.py

# This fixture is used to set up the test database before each test
@pytest.fixture(autouse=True)
async def setup_database():
    # Call the startup event function to initialize the database
    await app.router.startup()

    yield  # Here, the test will run

    # Here you can add code to drop the test database if needed
    # This will be executed after the test finishes
    await app.router.shutdown()

# This client will be used in your tests
client = TestClient(app)

# Example of a test function using the above setup
@pytest.mark.asyncio
async def test_create_conversation():
    response = client.post(
        "/conversations",
        json={"name": "Test Conversation"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Conversation"
