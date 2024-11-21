from utils.insurance_helper import get_provider_ids_by_insurance

def test_get_provider_ids_by_insurance(mocker):
    # Mock the `db` object
    mock_db = mocker.patch("utils.insurance_helper.db")
    mock_db["provider-insurance"].distinct.return_value = ["provider1", "provider2"]

    # Call the function under test
    result = get_provider_ids_by_insurance("BlueCross")

    # Assert the result
    assert result == ["provider1", "provider2"]
    mock_db["provider-insurance"].distinct.assert_called_once_with(
        "provider_id", {"insurance_name": {"$regex": "BlueCross", "$options": "i"}}
    )
