import json

from flask import request
from flask_classful import FlaskView, route
from flask_api import status
from app.service.user import user_info_validator
from app.schema.user import CreateSchema


class UserView(FlaskView):
    """
    유저 Front side
    """
    @route("", methods=["GET"])
    def healthcheck(self):
        print(f"{request.data}")
        return ("HeathCheck",
                status.HTTP_200_OK)

    @route("", methods=["POST"])
    @user_info_validator
    def sing_up(self):
        user = CreateSchema().load(json.loads(request.data))

        if user is False:
            return ("Error",
                    status.HTTP_409_CONFLICT)

        return ("OK",
                status.HTTP_200_OK)

    def log_in(self):
        pass
