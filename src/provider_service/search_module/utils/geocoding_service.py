import requests

# Uses the U.S. census geocoding service
def geocode_location(street, city, state, zip_code):
    url = "https://geocoding.geo.census.gov/geocoder/locations/address"
    params = {
        "street": street,
        "city": city,
        "state": state,
        "zip": zip_code,
        "benchmark": "Public_AR_Current",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["result"]["addressMatches"]:
            match = data["result"]["addressMatches"][0]
            lat = match["coordinates"]["y"]
            lon = match["coordinates"]["x"]
            return lat, lon
        return None, None
    except requests.RequestException as e:
        print(f"Error during geocoding: {e}")
        return None, None