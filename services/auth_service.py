import bcrypt
from flask import jsonify
from flask import make_response
from flask_jwt_extended import create_access_token,set_access_cookies
from bson import ObjectId

def register_user(db, data):
    users = db['users']
    if users.find_one({"email": data.get('email')}):
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user = {
        "email": data['email'],
        "password": hashed_password,
        "KYCStatus": False,
        "Documents": {}
    }
    users.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

# def login_user(db, data):
#     users = db['users']
#     user = users.find_one({"email": data.get('email')})
#     if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
#         return jsonify({"message": "Invalid email or password"}), 401
#     access_token = create_access_token(identity={'email': user['email']})
#     response = make_response(jsonify({"message": "Login successful"}))
#     response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite='Strict')

#     return response




def login_user(db, data):
    users = db['users']
    user = users.find_one({"email": data.get('email')})
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({"message": "Invalid email or password"}), 401

    # Use email (or another unique identifier like user_id) as the identity
    access_token = create_access_token(identity=user['email'])  

    response = jsonify({"message": "Login successful"})
    set_access_cookies(response, access_token)  # Automatically sets the token cookie
    return response
