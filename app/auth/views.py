import json
from app.auth import auth_blueprint
from flask import jsonify, request
from app.models import User
from app import db

@auth_blueprint.route('/api/auth/register/', methods=['POST'])
def register_user():
    # return "This"
    try:
        username = request.json.get("username")
        try:
            password = request.json.get("password")
        except KeyError:
            return jsonify({"error": "missing password"})
    except KeyError:
        return jsonify({"error": "missing username"})
    ''' Confirm username and password not empty'''
    if not username or not password:
        return jsonify({"error": "username or password cannot be empty"})

    ''' Check if a user with a similar username exists '''
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"error": "Username already exists"})

    ''' Create user instance and save to database '''
    user = User(username=username)
    user.encrypt_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user created successfully", "username": username}), 201

@auth_blueprint.route('/api/auth/login/', methods=['POST'])
def login():
    # return "This"
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    if not username or not password:
        return jsonify({"error": "missing username or password"}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Invalid login credentials"})
    elif not user.verify_password(password):
        return jsonify({"error": "invalid password"})
    else:
        token = user.generate_auth_token().decode('utf-8')
        return jsonify({"message": "login successful", "username": user.username, "authentication_token": token}), 200

# edge cases here