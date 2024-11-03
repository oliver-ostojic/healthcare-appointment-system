from flask import Flask
from dotenv import load_dotenv
import os
from mongodb_connection import client, test_connection
from booking_module.routes.users import users_bp


def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)
    # Set secret key for the Flask app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # Test MongoDB connection
    test_connection()
    # Register blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    return app
