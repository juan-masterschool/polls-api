import pytest
import requests
from tests.conftest import BASE_URL

def test_health_check():
    """Test that the health endpoint returns healthy status"""
    # Act: Make request to health endpoint
    response = requests.get(url=f"{BASE_URL}/health")

    # Assert: Check status code
    assert response.status_code == 200

    # Assert: Check response body
    data = response.json()
    assert data["status"] == "healthy"

def test_create_poll(auth_token):
    """Test creating a public poll"""
    # Arrange: Poll data
    poll_data = {
        "question": "What is your favorite language?",
        "options": ["Python", "JavaScript", "Java"],
        "is_public": True,
        "requires_admin": False
    }

    # Act: Create poll
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(
        f"{BASE_URL}/polls",
        json=poll_data,
        headers=headers
    )

    # Assert: Check response
    assert response.status_code == 201
    data = response.json()
    assert data["question"] == poll_data["question"]
    assert data["is_public"] == True
    assert len(data["options"]) == 3
    assert "id" in data

