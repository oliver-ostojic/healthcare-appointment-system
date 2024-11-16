import os
import certifi
from bson.objectid import ObjectId, InvalidId
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from pymongo import MongoClient
from src.user_service.mongodb_connection import users_collection, provider_schedules_collection
from ..models.appointment import Appointment, AppointmentStatus
from ..models.user import User
from ..models.schedule import Schedule
import jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
uri = os.getenv("MONGODB_URI")
# Set blueprint
users_bp = Blueprint('users_bp', __name__)
# Initialize MongoDB client
client = MongoClient(uri, tlsCAFile=certifi.where())


@users_bp.route('/', methods=['POST'])
def create_user():
    try:
        # Parse request and validate using User model
        user_data = request.get_json()
        if not user_data:
            return jsonify({'message': 'Missing or invalid JSON data'}), 400
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
    try:
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    except (InvalidId, ValueError):
        return jsonify({'message': 'Invalid user ID'}), 400
    if user_data:
        user_data['_id'] = str(user_data['_id'])
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@users_bp.route('/<user_id>/appointment', methods=['POST'])
def book_appointment(user_id):
    # Extract data from the request body
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing or invalid JSON data'}), 400
    # Extract appointment fields from the request body
    provider_id = data.get('provider_id')
    start_datetime = data.get('start_datetime')
    duration = data.get('duration')
    reason = data.get('reason')
    notes = data.get('notes')
    # Validate required fields
    if not provider_id or not start_datetime or not duration:
        return jsonify({'message': 'provider_id, start_datetime, and duration are required'}), 400
    # Create appointment object and dict
    else:
        appointment = Appointment(user_id=user_id,
                                  provider_id=provider_id,
                                  start_datetime=start_datetime,
                                  duration=duration,
                                  reason=reason,
                                  notes=notes)
        appointment_dict = appointment.model_dump()
    # Proceed with booking logic
    with client.start_session() as session:
        session.start_transaction()
        try:
            # Fetch the user's document from the collection
            user = users_collection.find_one({'_id': ObjectId(user_id)}, session=session)
            # Check in case user does not exist
            if not user:
                return jsonify({'message': 'User not found'}), 404
            # Fetch the provider's schedule
            provider_schedule_dict = provider_schedules_collection.find_one({'_id': ObjectId(provider_id)},
                                                                            session=session)
            # Covert dict to object
            provider_schedule = Schedule(**provider_schedule_dict)
            # Check in case provider_schedule does not exist
            if not provider_schedule:
                return jsonify({'message': 'Provider schedule not found'}), 404
            # Check that the slot is still available in the schedule
            available = provider_schedule.is_slot_available(start_datetime)
            if not available:
                return jsonify({'message': 'Slot is not available'}), 404
            # Update schedule
            provider_schedules_collection.update_one({'provider_id': provider_id},
                                                     {'$set': {'availability.$[slot].is_booked': True}},
                                                     array_filters=[{'slot.start_datetime': start_datetime}],
                                                     session=session)
            # Add new appointment
            result = users_collection.update_one({'_id': ObjectId(user_id)},
                                                 {'$push': {'appointments': appointment_dict}},
                                                 session=session)
            # Close session
            session.commit_transaction()
            return jsonify({'message': 'Appointment successfully booked'}), 200
        except Exception as e:
            session.abort_transaction()
            return jsonify({'error': str(e)}), 500


@users_bp.route('/<user_id>/appointment/<apt_id>', methods=['DEL'])
def cancel_appointment(user_id, apt_id):
    # Extract data from the request body
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing or invalid JSON data'}), 400
    # Proceed with canceling appointment logic
    with client.start_session() as session:
        session.start_transaction()
        try:
            # Get the user data
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            if not user or 'appointments' not in user:
                return jsonify({'message': 'User or Appointment not found'}), 404
            # Find the specific appointment with apt_id
            appointment = next((apt for apt in user['appointments'] if apt['_id'] == ObjectId(apt_id)), None)
            if not appointment:
                return jsonify({'message': 'Appointment not found'}), 404
            # Delete appointment with apt_id
            users_collection.update_one({'_id': ObjectId(user_id)},
                                        {'$pull': {'appointments': {'_id': ObjectId(apt_id)}}},
                                        session=session)
            # Get the provider_id from the appointment
            provider_id = appointment.get('provider_id')
            # Get the start time from the appointment
            start_datetime = appointment.get('start_datetime')
            # Update the provider's schedule to update appointment time_slot status
            provider_schedules_collection.update_one({'provider_id': provider_id},
                                                     {'$set': {'availability.$[slot].is_booked': False}},
                                                     array_filters=[{'slot.start_datetime': start_datetime}],
                                                     session=session)
            # Close session
            session.commit_transaction()
            return jsonify({'message': 'Appointment successfully booked'}), 200
        except Exception as e:
            session.abort_transaction()
            return jsonify({'error': str(e)}), 500
