from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient
import bcrypt
import requests
#from dotenv import load_dotenv

# Load environment variables from .env.local
#load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect(app)
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

# Hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

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

collection = db["patient-accounts"]    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        if collection.find_one({'username': username}):
            return jsonify({"error": "Username already exists"}), 400
        
        hashed_password = hash_password(password)
        
        # Insert new user
        collection.insert_one({'username': username, 'password': hashed_password})
        return jsonify({"message": "User registered successfully"}), 201

    return render_template('register.html')  # Add a register.html file for the form

limiter = Limiter(get_remote_address, app=app)
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate user credentials
        user = collection.find_one({'username': username})
        if user and verify_password(password, user['password'].encode('utf-8')):
            session['user'] = username
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    return render_template('login.html')  # Add a login.html file for the form

@app.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"}), 200

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
        taxonomy_doc = db["specialty"].find_one({"display_name": {"$regex": specialty, "$options": "i"}})
        if taxonomy_doc:
            taxonomy_code = taxonomy_doc.get("code")
            query["taxonomy_codes"] = {"$in": [taxonomy_code]}  # Check if taxonomy_code is in the array
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