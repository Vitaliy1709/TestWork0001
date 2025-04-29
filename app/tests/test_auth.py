import pytest


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post("/auth/register", json={
        "name": "testuser2",
        "email": "testuser2@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.asyncio
async def test_login(client, registered_user):
    response = await client.post("/auth/login", data={
        "username": registered_user["email"],
        "password": registered_user["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_refresh_token(client, registered_user):
    response = await client.post("/auth/login", data={
        "username": registered_user["email"],
        "password": registered_user["password"]
    })
    refresh_token = response.json()["refresh_token"]

    refresh_response = await client.post("/auth/refresh", headers={
        "Authorization": f"Bearer {refresh_token}"
    })

    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()
