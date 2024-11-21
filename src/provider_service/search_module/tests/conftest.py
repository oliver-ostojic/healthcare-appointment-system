import pytest
from app import app

@pytest.fixture
def client():
    """Fixture to create a test client for Flask."""
    with app.test_client() as client:
        yield client