from fastapi.testclient import TestClient
from singularity import app

client = TestClient(app)


def test_read_root():
    """Test that the root endpoint returns the expected response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_root_method_not_allowed():
    """Test that POST requests to the root endpoint are not allowed."""
    response = client.post("/")
    assert response.status_code == 405  # Method Not Allowed


def test_nonexistent_endpoint():
    """Test that requests to nonexistent endpoints return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
