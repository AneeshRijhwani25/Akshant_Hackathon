from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from config import Config
from services.auth_service import register_user, login_user
from services.user_service import get_user_by_pan, get_user_by_driving_licence, validate_and_save_document
from flask_jwt_extended import JWTManager, jwt_required
from services.ocr_service import convert_bytecode_to_image, extract_document_details, perform_ocr


app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

# MongoDB initialization
client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['DB_NAME']]

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(db, data)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(db, data)

@app.route('/user/pan', methods=['GET'])
def get_user_pan():
    pan_card_number = request.args.get('panCardNumber')
    user = get_user_by_pan(db, pan_card_number)
    if user:
        return jsonify({"user": user}), 200
    return jsonify({"message": "No user found with this PAN card number"}), 404

@app.route('/user/driving_licence', methods=['GET'])
def get_user_licence():
    driving_licence_number = request.args.get('drivingLicenceNumber')
    user = get_user_by_driving_licence(db, driving_licence_number)
    if user:
        return jsonify({"user": user}), 200
    return jsonify({"message": "No user found with this driving licence number"}), 404

@app.route('/validate/document', methods=['POST'])
def validate_document():
    data = request.get_json()
    return validate_and_save_document(db, data)


# @app.route('/ocr', methods=['POST'])
# def ocr_route():
#     """
#     OCR endpoint to process image bytecode and return extracted details.
#     """
#     try:
#         data = request.get_json()
#         image_bytecode = data.get('imageByteCode')

#         if not image_bytecode:
#             return jsonify({"message": "Image bytecode is missing"}), 400

#         # Convert bytecode to an image
#         image = convert_bytecode_to_image(image_bytecode)
        
#         reader = easyocr.Reader(['en'])
#         # Perform OCR
#         results = reader.readtext(image)
#         print("results---------------------------------------------------------")
#         print(results)
#         # Extract specific details from the results
#         document_details = extract_document_details(results)

#         return jsonify({"message": "OCR successful", "data": document_details}), 200
#     except Exception as e:
#         return jsonify({"message": "OCR failed", "error": str(e)}), 500

@app.route('/ocr', methods=['POST'])
def ocr_image():
   
    try:
        # Get image bytecode from the request
        data = request.get_json()
        image_bytecode = data.get("imageByteCode")
        if not image_bytecode:
            return jsonify({"error": "No image bytecode provided"}), 400

        # Convert bytecode to an image and save it locally
        output_path = "uploaded_image.png"
        convert_bytecode_to_image(image_bytecode, output_path)

        # Perform OCR on the saved image
        results = perform_ocr(output_path)

        # Extract details from OCR results
        document_details = extract_document_details(results)

        return jsonify({"data": document_details, "message": "OCR successful"}), 200
    except ValueError as e:
        return jsonify({"error": str(e), "message": "OCR failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e), "message": "An unexpected error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True)
