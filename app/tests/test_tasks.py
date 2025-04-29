import pytest


@pytest.mark.asyncio
async def test_create_task(client, access_token):
    response = await client.post("/tasks/tasks", headers={
        "Authorization": f"Bearer {access_token}"
    }, json={
        "title": "Test Task",
        "description": "Test Description",
        "priority": 2
    })
    assert response.status_code == 201
    assert "id" in response.json()


@pytest.mark.asyncio
async def test_update_task(client, access_token):
    create_response = await client.post(
        "/tasks/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Initial Task",
            "description": "Initial Description",
            "priority": 1
        }
    )
    task_id = create_response.json()["id"]
    # Updating a task by ID.
    update_response = await client.put(
        f"/tasks/tasks/{task_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Updated Title",
            "description": "Updated Description",
            "priority": 3
        }
    )
    assert update_response.status_code == 200


@pytest.mark.asyncio
async def test_get_tasks(client, access_token):
    response = await client.get("/tasks/tasks", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_search_tasks(client, access_token):
    response = await client.get("/tasks/tasks/search", headers={
        "Authorization": f"Bearer {access_token}"
    }, params={"q": "Test"})
    assert response.status_code == 200
