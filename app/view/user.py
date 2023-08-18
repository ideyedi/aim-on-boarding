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
    #@user_info_validator
    def sing_up(self):
        """
        request data type
        Content-Type: application/json
        Data-Raw JSON
        """
        print(f"id: {request.get_json()}")
        user = CreateSchema().load(json.loads(request.data))
        if user is False:
            return ("Error",
                    status.HTTP_409_CONFLICT)

        # 그냥 스키마 객체를 저장하면 바로 연결된 몽고에 들어가네
        # 진짜 편하게 잘 만들어짐..
        user.save()
        return ("OK",
                status.HTTP_200_OK)

    @route("login", methods=["POST"])
    def log_in(self):
        print(f"{request}")
        print(f"{request.data}")
        return ("OK",
                status.HTTP_200_OK)
