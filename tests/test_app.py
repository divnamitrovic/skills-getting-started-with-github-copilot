import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # First signup should succeed
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    # Second signup should fail (already signed up)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"

def test_remove_participant():
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # Signup first
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Remove participant
    response = client.delete(f"/activities/{activity}/remove", params={"email": email})
    assert response.status_code == 200
    # Try removing again (should fail)
    response = client.delete(f"/activities/{activity}/remove", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up"
