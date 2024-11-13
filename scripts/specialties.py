import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("")
db = client["MedConnect"]
specialty_collection = db["specialty"]

# Load data from CSV
df = pd.read_csv("nucc_taxonomy_241.csv")  # Replace with the path to your CSV file

# Extract the required columns and remove duplicates
df = df[['Specialization', 'Code', 'Display Name']].drop_duplicates(subset=['Code'])
# Convert each row to a dictionary and insert it into MongoDB
for _, row in df.iterrows():
    specialty_document = {
        "specialization": row['Specialization'],
        "code": row['Code'],
        "display_name": row['Display Name']
    }
    # Insert the document only if it does not already exist (ensure uniqueness)
    specialty_collection.update_one(
        {"code": row['Code']},  # Check for existing document by code
        {"$setOnInsert": specialty_document},
        upsert=True  # Insert if not found
    )
