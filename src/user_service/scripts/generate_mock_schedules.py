import random
from datetime import datetime, timedelta
import json
from src.user_service.booking_module.models.schedule import Slot
from pymongo.mongo_client import MongoClient
import certifi
import os
from dotenv import load_dotenv
# This script will create schedules for the months of November and December 2024
# For demonstration and presentation purposes

# MongoDB Setup
load_dotenv()
uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME")
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client[db_name]
provider_schedules_collection = db["provider_schedules"]

# Get the directory of the script
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "provider_ids.json")

# Load provider_ids
with open(file_path, "r") as f:
    provider_ids = json.load(f)


# Function to generate a mock schedule for a provider
def generate_mock_schedule(provider_id):
    # Available work days
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    # Choose random amount of work days
    num_days = random.choice(range(1, 2))
    # Choose random working days using num_days
    working_days = random.sample(days_of_week, num_days)
    # Initialize availability variable for schedule
    availability = []

    # Define the start and end dates
    start_date = datetime.strptime('2024-12-01', '%Y-%m-%d')
    end_date = datetime.strptime('2024-12-31', '%Y-%m-%d')

    # Map day names to weekday index
    day_to_name_index = {day: i for i, day in enumerate(days_of_week)}
    # Start with first date
    current_date = start_date

    # Create slots for date range
    while current_date <= end_date:
        # Iterate through the working days for the week
        for work_day in working_days:
            # Calculate the date for the current workday
            curr_day_index = day_to_name_index[work_day]
            curr_work_date = current_date + timedelta(days=(curr_day_index - current_date.weekday()) % 7)
            # Check current work date is not out of bounds
            if curr_work_date < start_date or curr_work_date > end_date:
                continue
            # Initialize start_time and end_time
            current_time = datetime(
                year=curr_work_date.year,
                month=curr_work_date.month,
                day=curr_work_date.day,
                hour=8,
                minute=0
            )
            shift_duration = random.choice(range(4, 6))
            end_time = current_time + timedelta(hours=shift_duration)
            # Generate time slots for day
            while current_time < end_time:
                # Create slot
                slot = Slot(
                    start_datetime=current_time,
                    duration=timedelta(minutes=15),
                    is_booked=False
                )
                availability.append(slot.to_dict())
                # Move to the next 15-minute slot
                current_time = current_time + timedelta(minutes=15)
        # Now move to the next week
        current_date += timedelta(weeks=1)
    # Sort availability
    availability.sort(key=lambda x: x["start_datetime"])
    return {
        "availability": availability,
        "provider_id": provider_id
    }


# Bulk insert schedules
def generate_and_insert_schedules(provider_id_list):
    batch_size = 1000
    schedules_batch = []
    # Create and append schedules to batch
    for i, provider_id in enumerate(provider_id_list):
        schedule = generate_mock_schedule(provider_id)
        schedules_batch.append(schedule)
        # Insert batch when batch size is reached
        if len(schedules_batch) == batch_size:
            provider_schedules_collection.insert_many(schedules_batch)
            schedules_batch = []
            print("Inserted {}/{} schedules...".format(i + 1, len(provider_ids)))
    if schedules_batch:
        provider_schedules_collection.insert_many(schedules_batch)
        print("Inserted remaining {} schedules.".format(len(schedules_batch)))


# Run the test function
if __name__ == "__main__":
    print("Starting schedule generation for {} providers...".format(len(provider_ids)))
    generate_and_insert_schedules(provider_ids)
    print("All schedules generated and inserted into the collection.")
