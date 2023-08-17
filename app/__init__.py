from flask import Flask, Request
from flask_cors import CORS
from flask_api import status

from app.route.user import blueprint as user_bp


def create_app():
    app = Flask(__name__)

    CORS(send_wildcard=True,
         expose_headers=["content-disposition"],
         max_age=6000).init_app(app)

    app.register_blueprint(user_bp)

    @app.route("/actuator")
    def heath_check():
        """
        Health Check Endpoint
        :return:
        """
        return ("OK",
                status.HTTP_200_OK)

    return app
