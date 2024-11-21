import pytest
import sys
import os
sys.path.insert(0, os.path.abspath("C:/Users/al334/Documents/VSCode/design-project/src/provider_service"))
from app import app

@pytest.fixture
def client():
    """Fixture to create a test client for Flask."""
    with app.test_client() as client:
        yield client