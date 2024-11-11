from pymongo import MongoClient

client = MongoClient()
db = client["MedConnect"]

# Create index as usual
db["provider-data"].create_index([("geometry", "2dsphere")])
print("2dsphere index created on geometry.coordinates")
