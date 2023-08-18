import mongoengine as me

from flask import Flask, Request, jsonify
from flask_cors import CORS
from flask_api import status
from flask_swagger_ui import get_swaggerui_blueprint

from app.view.user import UserView
from app.route.user import blueprint as user_bp

import os
import json
import datetime

from config import DevelopConfig

SWAGGER_URL = "/swagger-ui"


def create_app():
    app = Flask(__name__)

    app.config['DATA_DIR'] = "static/"
    app.config["MONGODB_SETTINGS"] = {
        "db": "on_boarding"
    }

    CORS(send_wildcard=True,
         resources={r'*': {'origins': '*'}},
         expose_headers=["content-disposition"],
         max_age=6000).init_app(app)

    swagger_ui = get_swaggerui_blueprint(
        SWAGGER_URL,
        "http://localhost:5000/swagger.json",
        config={
            "app_name": "On-Boarding"
        },
    )
    #
    register_db()
    #
    # app.register_blueprint(user_bp)
    UserView.register(app, route_base="/user")

    @app.route("/actuator")
    def heath_check():
        """
        Health Check Endpoint
        :return:
        """
        return ("OK",
                status.HTTP_200_OK)

    @app.route("/swagger")
    def swagger():
        """
        Rendering swagger ui
        :return:
        """
        swagger_json = os.path.join(app.config['DATA_DIR'], "swagger.json")
        print(f" swagger path : {swagger_json}, {app.config['DATA_DIR']}")
        with open(swagger_json, "r") as f:
            return jsonify(json.load(f))

    app.register_blueprint(swagger_ui)

    return app


def register_db():
    """
    MongoEngine 셋업
    :return:
    """
    try:
        me.connect(host=DevelopConfig.mongo_url)
    except ConnectionError:
        print(f"{str(ConnectionError)}")
    except Exception as e:
        print(f"{str(e)}")
