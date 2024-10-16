from flask import Blueprint, request, jsonify
from pymongo import ReturnDocument
from bson import ObjectId

from .models import UserModel, ScheduleModel
from pydantic import ValidationError

users_routes = Blueprint('users', __name__)
schedules_routes = Blueprint('schedules', __name__)


# USER ROUTES

# Create a user
@users_routes.route('/', methods=['POST'])
def create_user():
    from app import db
    try:
        data = request.get_json()
        user = UserModel(**data)
        db.users.insert_one(user.model_dump(by_alias=True))
        return jsonify(user.model_dump()), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


# Read (Get) All Users
@users_routes.route('/', methods=['GET'])
def get_users():
    from app import db
    users = list(db.users.find())

    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users), 200
