from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from config import Config
from services.auth_service import register_user, login_user
from services.user_service import get_user_by_pan, get_user_by_driving_licence, validate_and_save_document
from flask_jwt_extended import JWTManager, jwt_required


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

if __name__ == '__main__':
    app.run(debug=True)
