from mongodb_connection import db

def get_taxonomy_code(specialty):
    """
    Look up the taxonomy code for a given specialty.
    """
    taxonomy_doc = db["specialty"].find_one({"display_name": {"$regex": specialty, "$options": "i"}})
    if taxonomy_doc:
        return taxonomy_doc.get("code")
    return None