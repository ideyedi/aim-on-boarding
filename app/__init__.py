import mongoengine as me
from flask import Flask
from flask_cors import CORS
from flask_api import status

from app.view import route_extension
from config import DevelopConfig


def create_app():
    app = Flask(__name__)

    app.config.update({"APISPEC_SPEC": DevelopConfig.APISPEC_SPEC,
                       "APISPEC_SWAGGER_URL": DevelopConfig.APISPEC_SWAGGER_URL,
                       "APISPEC_SWAGGER_UI_URL": DevelopConfig.APISPEC_SWAGGER_UI_URL
                       })

    app.config["DOC_TITLE"] = "Swagger-Classful"
    app.config["DOC_VERSION"] = "0.0.1"
    app.config["DOC_OPEN_API_VERSION"] = "3.0.2"

    CORS(send_wildcard=True,
         resources={r'*': {'origins': '*'}},
         expose_headers=["content-disposition"],
         max_age=6000).init_app(app)

    register_db()
    route_extension(app)

    @app.route("/actuator")
    def heath_check():
        """
        Health Check Endpoint
        """
        return ("OK",
                status.HTTP_200_OK)

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
