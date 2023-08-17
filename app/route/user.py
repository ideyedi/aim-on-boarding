from flask import Flask, request, Blueprint
from flask_api import status
from flask_apispec import doc, use_kwargs
from pydantic import ValidationError

from app.model.user import User as UserModel

blueprint = Blueprint("user", __name__, url_prefix="/user")


@blueprint.route("test", methods=["GET"])
def get_hello():
    return (__name__,
            status.HTTP_200_OK)


class UserAccount():
    @blueprint.route("", methods=["POST"])
    @doc(summary="유저 회원 가입")
    @use_kwargs(UserModel, location=["json"])
    def create(self):
        pass
