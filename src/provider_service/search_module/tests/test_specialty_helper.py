from unittest.mock import MagicMock
from utils.specialty_helper import get_taxonomy_code

def test_get_taxonomy_code_found():
    # Mock the database collection
    mock_db = MagicMock()
    mock_db["specialty"].find_one.return_value = {"display_name": "Cardiology", "code": "1234"}
    
    # Patch the `db` object
    result = get_taxonomy_code("Cardiology")
    
    # Assert the correct taxonomy code is returned
    assert result == "1234"

def test_get_taxonomy_code_not_found():
    # Mock the database collection to return None
    mock_db = MagicMock()
    mock_db["specialty"].find_one.return_value = None
    
    # Patch the `db` object
    result = get_taxonomy_code("UnknownSpecialty")
    
    # Assert None is returned
    assert result is None
