import pymongo
from flask import Flask, jsonify
from pymongo.errors import ConnectionFailure
import sys
from .routes import users_routes, schedules_routes
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

db = None


def create_app():
    # Global db
    global db
    # Initialize flask app
    app = Flask(__name__)
    # Database setup
    try:
        client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
    except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)
    db = client["healthcare-db"]

    # Root route that returns a JSON response
    @app.route('/')
    def index():
        # Return a JSON response
        return jsonify({"message": "Database running"}), 200

    # Register blueprints
    app.register_blueprint(users_routes, url_prefix='/users')
    app.register_blueprint(schedules_routes, url_prefix='/schedules')
    # Return the flask app instance
    return app
