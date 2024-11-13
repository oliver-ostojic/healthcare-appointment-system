from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("")
db = client["MedConnect"]
provider_collection = db["provider-data"]

# Print all field names in a sample document
# sample_provider = provider_collection.find_one()
# if sample_provider:
#     print("Field names in sample document:")
#     for field in sample_provider.keys():
#         print(field)
# else:
#     print("No documents found in collection.")

# Update each document to consolidate taxonomy codes
for provider in provider_collection.find():
    taxonomy_codes = []
    
    # Access nested fields within 'properties'
    if "properties" in provider:
        for i in range(1, 16):
            field_name = f"Healthcare Provider Taxonomy Code_{i}"
            if field_name in provider["properties"]:  # Check if the field exists in properties
                code = provider["properties"][field_name]
                print(f"Found field {field_name}: {code}")  # Debugging output

                # Append valid codes that are not "None"
                if code and code != "None":
                    taxonomy_codes.append(code)
            else:
                print(f"Field {field_name} not found in 'properties' for document with _id: {provider['_id']}")

    # Debugging: print the final consolidated list of taxonomy codes
    print("Final taxonomy_codes list for provider:", taxonomy_codes)

    # Only update if there are valid taxonomy codes
    if taxonomy_codes:
        provider_collection.update_one(
            {"_id": provider["_id"]},
            {"$set": {"taxonomy_codes": taxonomy_codes}}
        )