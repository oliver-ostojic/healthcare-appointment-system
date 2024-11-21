from utils.insurance_helper import get_provider_ids_by_insurance
from unittest.mock import MagicMock

def test_get_provider_ids_by_insurance():
    mock_db = MagicMock()
    mock_db["provider-insurance"].distinct.return_value = ["provider1", "provider2"]

    result = get_provider_ids_by_insurance("BlueCross", mock_db)
    assert result == ["provider1", "provider2"]
    mock_db["provider-insurance"].distinct.assert_called_once_with(
        "provider_id", {"insurance_name": {"$regex": "BlueCross", "$options": "i"}}
    )
