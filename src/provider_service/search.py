from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from geocode import geocode_location  # Replace with your actual geocoding import

# Initialize MongoDB client (replace connection details with your own)
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']

# Create a Blueprint
provider_services_bp = Blueprint('provider_services_bp', __name__)

@provider_services_bp.route('/api/search', methods=['POST', 'OPTIONS'])
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
                "$maxDistance": radius_meters
            }
        }
    }

    # Look up the taxonomy code for the given specialty
    if specialty:
        taxonomy_doc = db["specialty"].find_one({"display_name": {"$regex": specialty, "$options": "i"}})
        if taxonomy_doc:
            taxonomy_code = taxonomy_doc.get("code")
            query["taxonomy_codes"] = {"$in": [taxonomy_code]}
        else:
            return jsonify({"error": "Specialty not found"}), 400

    # Add insurance filter if provided
    if insurance:
        provider_ids = db["provider-insurance"].distinct(
            "provider_id", {"insurance_name": {"$regex": insurance, "$options": "i"}}
        )
        if not provider_ids:
            return jsonify({"error": "No providers accept this insurance"}), 404
        query["_id"] = {"$in": provider_ids}

    try:
        results = list(db["provider-data"].find(query))
        return jsonify(results), 200
    except Exception as e:
        print("Error querying the database:", e)
        return jsonify({"error": str(e)}), 500