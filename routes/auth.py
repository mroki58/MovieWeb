from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
)
import bcrypt

from repositories.UserRepository import UserRepo

auth_bp = Blueprint("auth", __name__, url_prefix="/")


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "msg": "Username and password required"}), 400

    hashed_pw, idx = UserRepo.find_users_id_password_by_username(username)

    if bcrypt.checkpw(password.encode("utf-8"), hashed_pw):
        access_token = create_access_token(identity=idx)
        resp = jsonify({"success": True, "msg": "Logged in successfully"})
        set_access_cookies(resp, access_token)
        return resp

    return jsonify({"success": False, "msg": "Invalid username or password"}), 401


@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    interests = data.get("interests", [])

    if not username or not password or not email:
        return jsonify({"success": False, "msg": "Username, password and email required"}), 400

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

    if UserRepo.is_user_registered(username):
        return jsonify({"success": False, "msg": "Username already registered"}), 400


    idx = UserRepo.register_user(
        username=username,
        email=email,
        password=hashed_pw
    )

    if interests:
        UserRepo.add_interests_for_user(idx, interests)

    return jsonify({"success": True, "msg": "User registered successfully"}), 201
