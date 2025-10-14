from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
)
import bcrypt
from db.init_db import get_driver
from uuid import uuid4

auth_bp = Blueprint("auth", __name__, url_prefix="/")


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "msg": "Username and password required"}), 400

    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {username:$username}) RETURN u.password AS password, u.id AS id",
            username=username
        )
        record = result.single()
        if record:
            hashed_pw = record["password"].encode("utf-8")
            idx = record["id"]
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

    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {username:$username}) RETURN u",
            username=username
        )
        if result.single():
            return jsonify({"success": False, "msg": "User already exists"}), 409

        session.run(
            """
            CREATE (u:User {
                id:$id,
                username:$username,
                password:$password,
                email:$email
            })
            """,
            id=str(uuid4()),
            username=username,
            password=hashed_pw,
            email=email
        )

        if interests:
            session.run(
                """
                MATCH (u:User {username:$username})
                UNWIND $interests AS interest_name
                MATCH (g:Genre {name: interest_name})
                MERGE (u)-[:HAS_INTEREST]->(g)
                """,
                username=username,
                interests=interests
            )

    return jsonify({"success": True, "msg": "User registered successfully"}), 201
