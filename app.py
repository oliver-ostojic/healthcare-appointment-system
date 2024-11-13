from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
#import os
import requests
#from dotenv import load_dotenv

# Load environment variables from .env.local
#load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
client = MongoClient("mongodb+srv://al6894:design@dev-cluster.7q4va.mongodb.net/")
db = client.MedConnect

# Test the connection by listing the collections in your database
try:
    collections = db.list_collection_names()
    print("Collections in the database:", collections)
except Exception as e:
    print("Error connecting to the database:", e)
    
# indexes = db["provider-data"].index_information()
# print("Indexes on provider-data collection:", indexes)


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
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract latitude and longitude from the response
    if data["result"]["addressMatches"]:
        match = data["result"]["addressMatches"][0]
        lat = match["coordinates"]["y"]
        lon = match["coordinates"]["x"]
        return lat, lon
    else:
        return None, None

@app.route('/api/search', methods=['POST', 'OPTIONS'])
def search():
    if request.method == 'OPTIONS':
        # This handles the CORS preflight request
        return '', 204
    data = request.get_json()
    street = data.get("street")
    city = data.get("city")
    state = data.get("state")
    zip_code = data.get("zip")
    specialty = data.get("specialty")
    insurance = data.get("insurance")
    radius_miles = data.get("radius", 10)  # Radius in miles

    radius_miles = 10
    # Convert radius from miles to meters
    radius_meters = radius_miles * 1609.34

    # Geocode the location to get latitude and longitude
    lat, lon = geocode_location(street, city, state, zip_code)
    
    if lat is None or lon is None:
        return jsonify({"error": "Location not found"}), 400

    # Build MongoDB query with geospatial and additional conditions
    query = {
        "geometry": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "$maxDistance": radius_meters  # Use radius in meters
            }
        }
    }
    # Look up the taxonomy code for the given specialty
    if specialty:
        taxonomy_doc = db["specialty"].find_one({"name": {"$regex": specialty, "$options": "i"}})
        if taxonomy_doc:
            taxonomy_code = taxonomy_doc.get("taxonomy_code")
            query["taxonomy_code"] = taxonomy_code
        else:
            return jsonify({"error": "Specialty not found"}), 400

    # Add insurance filter if provided
    if insurance:
        query["insurance"] = {"$regex": insurance, "$options": "i"}

    try:
        results = list(db["provider-data"].find(query))
        print("Query results:", results)
        return jsonify(results), 200
    except Exception as e:
        print("Error querying the database:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)