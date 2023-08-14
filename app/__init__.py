from flask import Flask, Request
from flask_cors import CORS
from flask_api import status


def create_app():
    app = Flask(__name__)

    CORS(send_wildcard=True,
         expose_headers=["content-disposition"],
         max_age=6000).init_app(app)

    @app.route("/")
    def heath_check():
        return "{status.HTTP_200_OK}"

    return app
