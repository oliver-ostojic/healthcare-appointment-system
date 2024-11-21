from mongodb_connection import db

def get_provider_ids_by_insurance(insurance):
    """
    Find provider IDs that match the given insurance name.
    """
    provider_ids = db["provider-insurance"].distinct(
        "provider_id", {"insurance_name": {"$regex": insurance, "$options": "i"}}
    )
    return provider_ids