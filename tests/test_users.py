import uuid
import unittest
import sys
from fastapi.testclient import TestClient
sys.path.append('/Users/cyliahamdi/Desktop/DoList')  
from classes.schema_dto import User, UserNoID
from main import app

client = TestClient(app)

def test_create_user():
    user_data = {
        "givenName": "newuser",
        "email": "user@example.com",
        "givenPassword": "newpassword"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    return response.json()['id']

def test_get_user():
    user_id = test_create_user() 
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200


def test_update_user():
    user_id = test_create_user()  # Create a new user to update
    updated_user_data = {"username": "updateduser"}
    response = client.patch(f"/users/{user_id}", json=updated_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"

def test_delete_user():
    user_id = test_create_user()  # Create a new user to delete
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    # Verify user is deleted
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
