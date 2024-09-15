import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, get_db


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the database for testing
Base.metadata.create_all(bind=engine)

# Dependency override for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

# Test creating an article
def test_create_article(test_client):
    response = test_client.post("/articles/", json={
        "title": "Test Article",
        "content": "This is a test article.",
        "author": "Test Author",
        "category": "Test Category"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Article"
    assert response.json()["author"] == "Test Author"

# Test retrieving an article
def test_read_article(test_client):
    article_id = 1  # Assuming the article with id 1 exists
    response = test_client.get(f"/articles/{article_id}")
    assert response.status_code == 200
    assert response.json()["id"] == article_id

# Test listing articles
def test_list_articles(test_client):
    response = test_client.get("/articles/")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Test updating an article
def test_update_article(test_client):
    article_id = 1  # Assuming the article with id 1 exists
    response = test_client.put(f"/articles/{article_id}", json={
        "title": "Updated Test Article",
        "content": "Updated content",
        "author": "Test Author",
        "category": "Updated Category"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Article"
    assert response.json()["category"] == "Updated Category"

# Test deleting an article
def test_delete_article(test_client):
    article_id = 1  # Assuming the article with id 1 exists
    response = test_client.delete(f"/articles/{article_id}")
    assert response.status_code == 200

# Test adding a comment to an article
def test_create_comment(test_client):
    article_id = 1  # Assuming the article with id 1 exists
    response = test_client.post(f"/articles/{article_id}/comments/", json={
        "content": "This is a test comment."
    })
    assert response.status_code == 200
    assert response.json()["content"] == "This is a test comment."
