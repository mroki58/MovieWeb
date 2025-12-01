from ariadne.explorer import ExplorerApollo
from ariadne import graphql_sync

import atexit
from datetime import timedelta

from flask import Flask, request, jsonify, Response
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager
import jwt as pyjwt

from gql.error_formatter import custom_error_formatter
from gql.schema import schema

from db.init_db import close_driver
from routes.auth import auth_bp

class APSConfig:
    SCHEDULER_API_ENABLED = False

app = Flask(__name__)
app.config.from_object(APSConfig)
app.config["JWT_SECRET_KEY"] = "secret"
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_SAMESITE"] = "Lax"
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)
app.register_blueprint(auth_bp)

scheduler = APScheduler()
scheduler.init_app(app)

playground = ExplorerApollo(include_cookies=True)

@app.route("/graphql", methods=["GET"])
def gql_interface():
    return Response(playground.html(request), mimetype="text/html")

@app.route("/graphql", methods=["POST"])
def graphql_server():
    try:
        token = request.cookies.get("access_token_cookie")
        payload = pyjwt.decode(token, app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        userId = payload['sub']
    except Exception as e:
        print("JWT error:", e)
        userId = None

    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request, "userId": userId},
        debug=True,
        error_formatter=custom_error_formatter
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

atexit.register(close_driver)

@scheduler.task('interval', id='recalculate_movie_avgs', minutes=5, max_instances=1)
def revalc_job():
    from scripts.recalculate_movie_ratings import main as recalc_avgs
    recalc_avgs()


if __name__ == '__main__':
    scheduler.start()
    app.run()
