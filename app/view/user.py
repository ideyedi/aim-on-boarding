import json

from flask import request
from flask_apispec import marshal_with
from flask_classful import FlaskView, route
from flask_api import status

from app.service.user import user_info_validator, UserService
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
    #@marshal_with(CreateSchema)
    @user_info_validator
    def sing_up(self):
        """
        request data type
        Content-Type: application/json
        Data-Raw JSON
        """
        user = CreateSchema().load(json.loads(request.data))
        if user is False:
            return ("Error",
                    status.HTTP_409_CONFLICT)

        user_service = UserService(user)
        ret = user_service.sign_up()
        if ret is not status.HTTP_200_OK:
            return ("Login Failed",
                    ret)

        return ("OK",
                status.HTTP_200_OK)

    @route("login", methods=["POST"])
    def log_in(self):
        print(f"{request}")
        print(f"{request.data}")
        return ("OK",
                status.HTTP_200_OK)
