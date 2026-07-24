"""Tests for Task Manager API endpoints."""

import pytest


def register_user(client):
    """Helper function to create a test user."""

    response = client.post(
        "/auth/register",
        json={
            "name": "testuser",
            "email": "test@example.com",
            "password": "Password123!",
        },
    )

    return response


def get_auth_headers(client):
    """Helper function to register and return JWT headers."""

    response = client.post(
        "/auth/register",
        json={
            "name": "testuser",
            "email": "test@example.com",
            "password": "Password123!",
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_health_check(client):
    """Health check returns 200."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_user(client):
    """User registration returns a JWT token."""

    response = register_user(client)

    assert response.status_code == 201

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_create_task_authenticated(client):
    """Authenticated users can create tasks."""

    headers = get_auth_headers(client)

    response = client.post(
        "/tasks/",
        headers=headers,
        json={
            "title": "Finish FastAPI project",
            "description": "Complete Module 5 Task Manager",
            "priority": "high",
            "completed": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Finish FastAPI project"
    assert data["priority"] == "high"


def test_authentication_required(client):
    """Protected endpoints reject unauthenticated users."""

    response = client.get("/tasks/")

    assert response.status_code == 401


def test_list_tasks(client):
    """Authenticated users can list their tasks."""

    headers = get_auth_headers(client)

    client.post(
        "/tasks/",
        headers=headers,
        json={
            "title": "Task One",
            "priority": "medium",
            "completed": False,
        },
    )

    response = client.get(
        "/tasks/",
        headers=headers,
    )

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task One"


def test_get_task(client):
    """Authenticated users can retrieve their own task."""

    headers = get_auth_headers(client)

    create_response = client.post(
        "/tasks/",
        headers=headers,
        json={
            "title": "Read documentation",
            "priority": "low",
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_task_not_found(client):
    """Requesting a missing task returns 404."""

    headers = get_auth_headers(client)

    response = client.get(
        "/tasks/9999",
        headers=headers,
    )

    assert response.status_code == 404


def test_post_task_suggest(client):
    """AI suggestion endpoint returns placeholder response."""

    headers = get_auth_headers(client)

    create_response = client.post(
        "/tasks/",
        headers=headers,
        json={
            "title": "Plan workout",
            "priority": "medium",
        },
    )

    task_id = create_response.json()["id"]

    response = client.post(
    f"/tasks/{task_id}/suggest",
    headers=headers,
    json={
        "description": "How can I complete this task efficiently?"
    },
)

    assert response.status_code == 200

    data = response.json()

    assert "suggestion" in data
    assert data["ai_ready"] is True