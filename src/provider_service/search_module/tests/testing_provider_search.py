def test_search_route(client, mocker):
    # Mock geocoding_service
    mocker.patch("routes.search.geocoding_service", return_value=(38.8977, -77.0365))

    # Mock MongoDB queries
    mocker.patch("routes.search.search_specialty", return_value={"code": "1234"})
    mocker.patch("routes.search.search_insurance", return_value=["provider1", "provider2"])

    # Mock MongoDB find query
    mocker.patch("routes.search.db['provider-data'].find", return_value=[
        {"_id": "provider1", "name": "Provider One"},
        {"_id": "provider2", "name": "Provider Two"}
    ])

    # Test search with valid data
    response = client.post("/providers/search", json={
        "street": "1600 Pennsylvania Ave NW",
        "city": "Washington",
        "state": "DC",
        "zip": "20500",
        "specialty": "Cardiology",
        "insurance": "BlueCross",
        "radius": 10
    })
    assert response.status_code == 200
    assert response.json == [
        {"_id": "provider1", "name": "Provider One"},
        {"_id": "provider2", "name": "Provider Two"}
    ]
