from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
)
from flask_jwt_extended import unset_jwt_cookies
import bcrypt

from repositories.UserRepository import UserRepo
from flask import current_app
import jwt as pyjwt

auth_bp = Blueprint("auth", __name__, url_prefix="/")


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "msg": "Username and password required"}), 400

    hashed_pw, idx = UserRepo.find_users_id_password_by_username(username)

    if idx == 'err':
        return jsonify({"success": False, "msg": "Username not found"}), 404

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


@auth_bp.route('/logged', methods=['GET'])
def logged():
    try:
        token = request.cookies.get(current_app.config.get("JWT_ACCESS_COOKIE_NAME", "access_token_cookie"))
        if not token:
            return jsonify({"logged": False})
        payload = pyjwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        userId = payload.get('sub')
        return jsonify({"logged": True if userId else False})
    except Exception:
        return jsonify({"logged": False})


@auth_bp.route('/logout', methods=['POST'])
def logout_route():
    resp = jsonify({"success": True, "msg": "Logged out"})
    try:
        unset_jwt_cookies(resp)
    except Exception:
        cookie_name = current_app.config.get("JWT_ACCESS_COOKIE_NAME", "access_token_cookie")
        resp.set_cookie(cookie_name, '', expires=0, path='/')

    try:
        cookie_name = current_app.config.get("JWT_ACCESS_COOKIE_NAME", "access_token_cookie")
        resp.delete_cookie(cookie_name, path='/')
    except Exception:
        pass
    return resp
