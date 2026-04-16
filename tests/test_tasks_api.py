import pytest

def test_get_tasks_returns_seeded_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    payload = response.get_json()
    assert len(payload) >= 2  # בודק שיש לפחות את משימות הבסיס

def test_get_task_by_id_returns_single_task(client):
    # שולף ID קיים מהרשימה
    all_tasks = client.get("/tasks").get_json()
    task_id = all_tasks[0]["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["id"] == task_id

def test_get_task_by_id_returns_404_for_missing_task(client):
    response = client.get("/tasks/missing_id")
    assert response.status_code == 404
    payload = response.get_json()
    # התאמה למבנה ה-Global Handler החדש:
    assert payload["error"] == "Not Found"
    assert "not found" in payload["message"].lower()
    assert payload["status"] == 404

def test_create_task_trims_title_and_returns_created_resource(client):
    response = client.post("/tasks", json={"title": "  Write tests  "})
    assert response.status_code == 201
    payload = response.get_json()
    # בהתאם ל-Routes שלך, המשימה חוזרת ישירות
    assert payload["title"] == "Write tests"
    assert payload["completed"] is False

def test_create_task_requires_json_body(client):
    # שליחת בקשה ללא Content-Type: application/json
    response = client.post("/tasks", data="not a json")
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["error"] == "Bad Request"
    assert payload["status"] == 400

def test_create_task_rejects_blank_title(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422
    payload = response.get_json()
    assert payload["error"] == "Unprocessable Entity"
    assert "title" in payload["message"].lower()

def test_update_task_changes_title_and_completed_flag(client):
    all_tasks = client.get("/tasks").get_json()
    task_id = all_tasks[0]["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated task", "completed": True},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["title"] == "Updated task"
    assert payload["completed"] is True

def test_delete_task_removes_existing_task(client):
    all_tasks = client.get("/tasks").get_json()
    task_id = all_tasks[0]["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # וידוא שהמשימה באמת נמחקה
    follow_up = client.get(f"/tasks/{task_id}")
    assert follow_up.status_code == 404