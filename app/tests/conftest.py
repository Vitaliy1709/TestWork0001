from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.test")
from typing import Any, AsyncGenerator
from httpx import ASGITransport

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.models.base import Base

test_engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)


# Dependency override
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides = {}
from app.db.session import get_db

app.dependency_overrides[get_db] = override_get_db


# Create tables before all tests
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# Session
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with TestSessionLocal() as session:
        yield session


# HTTP client
@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        yield ac


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def registered_user(client):
    payload = {
        "name": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
    await client.post("/auth/register", json=payload)
    return payload


@pytest_asyncio.fixture
async def access_token(client, registered_user):
    login_data = {
        "username": registered_user["email"],
        "password": registered_user["password"]
    }
    response = await client.post("/auth/login", data=login_data)
    return response.json()["access_token"]
