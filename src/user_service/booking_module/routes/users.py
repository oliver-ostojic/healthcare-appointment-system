import os

from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from src.user_service.mongodb_connection import users_collection
from ..models.user import User
import jwt
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
# Set blueprint
users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/', methods=['POST'])
def create_user():
    try:
        # Parse request and validate using User model
        user_data = request.get_json()
        user = User(**user_data)
        # Convert Pydantic model to a dict
        user_dict = user.model_dump()
        # Insert into MongoDB and get inserted ID
        result = users_collection.insert_one(user_dict)
        # Return success response
        return jsonify({'message': 'User successfully created.', 'id': str(result.inserted_id)}), 201
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 422
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@users_bp.route('/<user_id>', methods=['GET'])
def get_user_info(user_id):
    # Extract the token from the header
    auth_header = request.headers.get('Authorization')
    # If the token is not present, return message
    if not auth_header:
        return jsonify({'message': 'Missing Authorization header'}), 401
    # Set token to variable by splitting at " " space
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    # Decode the token
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        token_user_id = decoded_token.get('id')
        # Compare the user_id GET request to token with user_id
        if user_id != token_user_id:
            return jsonify({'message': 'Forbidden, you are not allowed to access this resource'}), 403
        # If IDs match, fetch and return the requested user document from mongodb
        else:
            user_data = users_collection.find_one({'id': user_id})
            return jsonify({user_data}), 200
    # Else return error messages
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token is invalid'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500
