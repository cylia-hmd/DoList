import uuid
import unittest
import sys
from fastapi.testclient import TestClient
sys.path.append('/Users/cyliahamdi/Desktop/DoList')
from classes.schema_dto import Task, TaskNoID
from main import app

client = TestClient(app)

def test_create_task():
    task_data = {"title": "New Task", "description": "A new task description", "owner": "User1", "completed": False}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    return data["id"]

def test_get_task():
    task_id = test_create_task()  # Create a new task to test retrieval
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task():
    task_id = test_create_task()  # Create a new task to update
    updated_task_data = {"title": "Updated Task", "description": "Updated description", "completed": True}
    response = client.patch(f"/tasks/{task_id}", json=updated_task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"

def test_delete_task():
    task_id = test_create_task()  # Create a new task to delete
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    # Verify task is deleted
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
