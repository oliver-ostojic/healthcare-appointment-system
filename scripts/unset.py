from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("")
db = client["MedConnect"]
provider_collection = db["provider-data"]

# Create a dictionary with all nested fields to unset in 'properties'
fields_to_unset = {f"properties.Healthcare Provider Taxonomy Code_{i}": "" for i in range(1, 16)}
fields_to_unset.update({f"properties.Healthcare Provider Primary Taxonomy Switch_{i}": "" for i in range(1, 16)})
fields_to_unset.update({f"properties.Healthcare Provider Taxonomy Group_{i}": "" for i in range(1, 16)})

# Apply the unset operation to all documents
provider_collection.update_many({}, {"$unset": fields_to_unset})

print("Nested fields within 'properties' have been successfully removed.")
