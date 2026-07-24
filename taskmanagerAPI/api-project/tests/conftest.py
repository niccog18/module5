"""Pytest configuration and fixtures for Task Manager API tests."""

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


# In-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# -------------------------
# Database Fixture
# -------------------------

@pytest.fixture
def db_session():
    """
    Create a fresh database session for each test.

    Creates all tables before the test and removes
    them after the test completes.
    """

    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


# -------------------------
# FastAPI Client Fixture
# -------------------------

@pytest.fixture
def client(db_session):
    """
    Provide a TestClient using the test database.

    Overrides the production database dependency
    so tests never modify the real database.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# -------------------------
# Authentication Fixture
# -------------------------

@pytest.fixture
def auth_headers(client):
    """
    Register and authenticate a test user.

    Returns:
        Authorization headers containing JWT token.
    """

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }