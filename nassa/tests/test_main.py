import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from nassa.main import app, db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    db.clear()
    yield
    db.clear()


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "operational"


def test_create_task():
    payload = {"title": "Learn FastAPI", "description": "Build a simple API"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Build a simple API"
    assert data["status"] == "todo"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_invalid():
    # Empty title is invalid
    payload = {"title": "", "description": "Invalid task"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_get_tasks():
    # Insert a couple of tasks
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Task B should come first as it was created last (descending order)
    assert data[0]["title"] == "Task B"
    assert data[1]["title"] == "Task A"


def test_get_tasks_filter_status():
    # Insert tasks with different statuses
    resp_a = client.post("/tasks", json={"title": "Task A"})
    task_a_id = resp_a.json()["id"]
    
    # Update Task A to IN_PROGRESS
    client.put(f"/tasks/{task_a_id}", json={"status": "in_progress"})
    client.post("/tasks", json={"title": "Task B"})
    
    # Get only in_progress tasks
    response = client.get("/tasks?status=in_progress")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task A"


def test_get_task_by_id():
    resp = client.post("/tasks", json={"title": "Single Task"})
    task_id = resp.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Single Task"


def test_get_task_not_found():
    random_uuid = str(uuid4())
    response = client.get(f"/tasks/{random_uuid}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with ID {random_uuid} not found"


def test_update_task():
    resp = client.post("/tasks", json={"title": "Original Title", "description": "Original Desc"})
    task_id = resp.json()["id"]
    
    payload = {"title": "Updated Title", "status": "done"}
    response = client.put(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Original Desc"  # description should remain unchanged
    assert data["status"] == "done"


def test_delete_task():
    resp = client.post("/tasks", json={"title": "To Delete"})
    task_id = resp.json()["id"]
    
    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 204
    
    # Confirm it is deleted
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404
