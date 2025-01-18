from flask import jsonify,request
from bson.objectid import ObjectId
from utils.validators import validate_pan, validate_driving_licence
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from bson.json_util import dumps

def serialize_document(doc):
    """
    Recursively convert all ObjectId instances to strings,
    and convert bytes to strings (or exclude them if sensitive).
    """
    if isinstance(doc, dict):
        return {key: serialize_document(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [serialize_document(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, bytes):
        return doc.decode('utf-8')  # Convert bytes to a string
    else:
        return doc

def get_user_by_pan(db, pan_card_number):

    # Query the user by PAN card number
    user = db['users'].find_one({"Documents.panCardDetails.panCardNumber": pan_card_number})
    if user:
        # Serialize the document to ensure JSON compatibility
        user.pop('password', None)
        user = serialize_document(user)
        return user  # Return the serialized user document

    # If no user is found, return None
    return None


def get_user_by_driving_licence(db, driving_licence_number):
    user = db['users'].find_one({"Documents.DrivingLicenceDetails.drivingLicenceNumber": driving_licence_number})
    if user:
        # Serialize the document to ensure JSON compatibility
        user.pop('password', None)
        user = serialize_document(user)
        return user  # Return the serialized user document

    # If no user is found, return None
    return None



@jwt_required()  # Reads the token from the cookie
def validate_and_save_document(db, data):
    # Get the email from the JWT token
    user_email = get_jwt_identity()  

    users = db['users']
    user = users.find_one({"email": user_email})
    if not user:
        return jsonify({"message": "User not found"}), 404

    document_type = data.get("document_type")
    document_details = data.get("document_details")

    if document_type == "panCardDetails":
        if not validate_pan(document_details.get("panCardNumber")):
            return jsonify({"message": "Invalid PAN card details"}), 400
        user['Documents']['panCardDetails'] = document_details

    elif document_type == "DrivingLicenceDetails":
        if not validate_driving_licence(document_details.get("drivingLicenceNumber")):
            return jsonify({"message": "Invalid Driving Licence details"}), 400
        user['Documents']['DrivingLicenceDetails'] = document_details

    # Update the user's document in the database
    users.update_one({"_id": user["_id"]}, {"$set": {"Documents": user['Documents'], "KYCStatus": True}})
    return jsonify({"message": "Document validated and saved successfully"}), 200
