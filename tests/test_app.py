import pytest
from app import create_app
from app.models import *
import datetime


# Provides test client for the app
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_create_user(client):
    # Create address
    address = AddressModel(street='109 Saint Marks Pl', unit='18', city='New York', state='New York', zip='10009')
    # Create date of birth
    dob = datetime.date(2002, 6, 13)
    # Create insurance model
    insurance = InsuranceModel(member_id="12jd29k", company="Blue Cross")
    # Send a POST request to the /user route
    response = client.post('/users/', json={
        "name": "Oliver Ostojic",
        "email": "oliver.ostojic.swe@gmail.com",
        "address": address.model_dump(),
        "password_hash": "3918uec9h2",
        "date_of_birth": dob.isoformat(),
        "insurance": insurance.model_dump()
    })
    # Assert that the status code is 201
    assert response.status_code == 201
    # Check if the response contains the created user
    response_data = response.get_json()
    assert response_data["name"] == "Oliver Ostojic"
    assert response_data["email"] == "oliver.ostojic.swe@gmail.com"
    assert response_data["address"]["street"] == "109 Saint Marks Pl"
    assert response_data["address"]["city"] == "New York"
    assert response_data["address"]["state"] == "New York"
    assert response_data["address"]["zip"] == "10009"
    assert response_data["date_of_birth"] == dob.isoformat()
    assert response_data["insurance"]["member_id"] == "12jd29k"
    assert response_data["insurance"]["company"] == "Blue Cross"

