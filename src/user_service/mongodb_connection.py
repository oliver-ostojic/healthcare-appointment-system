from pymongo.mongo_client import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME")

client = MongoClient(uri, tlsCAFile=certifi.where())
db = client[db_name]
users_collection = db["users"]
provider_schedules_collection = db["provider_schedules"]


def test_connection():
    try:
        client.admin.command("ping")
        print("Pinged your deployment. Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
