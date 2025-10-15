from ariadne.explorer import ExplorerApollo
from ariadne import graphql_sync
from gql.schema import schema
import atexit

from flask import Flask, request, jsonify, Response
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity

from db.init_db import close_driver
from routes.auth import auth_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret"
jwt = JWTManager(app)
app.register_blueprint(auth_bp)

playground = ExplorerApollo(include_cookies=True)

@app.route("/graphql", methods=["GET"])
def gql_interface():
    return Response(playground.html(request), mimetype="text/html")

@app.route("/graphql", methods=["POST"])
def graphql_server():
    try:
        verify_jwt_in_request(optional=True)
        userId = get_jwt_identity()
    except:
        userId = None

    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request, "userId": userId},
        debug=True
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

atexit.register(close_driver)

if __name__ == '__main__':
    app.run()
