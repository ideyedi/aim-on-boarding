from flask import Flask, request, Blueprint
from flask_api import status
from pydantic import ValidationError

blueprint = Blueprint("user", __name__)


@blueprint.route("/user", methods=["GET"])
def get_hello():
    return (__name__,
            status.HTTP_200_OK)
