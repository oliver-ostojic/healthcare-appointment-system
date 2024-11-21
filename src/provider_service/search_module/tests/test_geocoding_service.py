import pytest
from utils.geocoding_service import geocode_location
import requests
from unittest.mock import patch

def test_geocode_location_success():
    mock_response = {
        "result": {
            "addressMatches": [
                {"coordinates": {"y": 38.8977, "x": -77.0365}}
            ]
        }
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        lat, lon = geocode_location("1600 Pennsylvania Ave NW", "Washington", "DC", "20500")
        assert lat == 38.8977
        assert lon == -77.0365

def test_geocode_location_no_matches():
    mock_response = {"result": {"addressMatches": []}}
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        lat, lon = geocode_location("Invalid Address", "Nowhere", "NA", "00000")
        assert lat is None
        assert lon is None

def test_geocode_location_api_error():
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        lat, lon = geocode_location("1600 Pennsylvania Ave NW", "Washington", "DC", "20500")
        assert lat is None
        assert lon is None
