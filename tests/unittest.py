import pytest
import sqlite3
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def setup_database():
    """In-memory test database to avoid modifying library.db."""
    conn = sqlite3.connect(":memory:")
    conn.execute("""CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, description TEXT, image_path TEXT, pdf_path TEXT)""")
    conn.executemany("INSERT INTO books (title, author, description, image_path, pdf_path) VALUES (?, ?, ?, ?, ?)", [
        ("My Book", "Author 1", "Description", "images/book1.jpg", "pdf/book1.pdf"),
        ("Sports Guide", "Author 2", "Description", "images/sports.jpg", "pdf/sports.pdf")
    ])
    conn.commit()
    yield conn
    conn.close()

def test_sports_page(client, setup_database):
    response = client.get('/sports')
    assert response.status_code == 200
    assert b"Sports Guide" in response.data

def test_dynamic_books(client, setup_database):
    response = client.get('/sports')
    assert b"My Book" in response.data
    assert b"Sports Guide" in response.data

