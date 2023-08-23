import json

from flask import request
from flask_apispec import marshal_with, doc, use_kwargs
from flask_classful import FlaskView, route
from flask_api import status
from marshmallow import fields

from app.service.user import user_info_validator, UserService
from app.schema.user import CreateSchema, LoginSchema, ModifySchema, UserSchema


class UserView(FlaskView):
    """
    유저 Front side
    """
    @doc(summary="user apis heathCheck")
    @route("", methods=["GET"])
    def healthcheck(self):
        print(f"{request.data}")
        return ("HeathCheck",
                status.HTTP_200_OK)

    shae = 2
    doc_string = f"{shae}, parameter 보이지 않는 문제 확인 필요합니다."

    @route("", methods=["POST"])
    @doc(description=doc_string, summary="유저 회원가입")
    @user_info_validator
    @use_kwargs(UserSchema, location="json")
    def sing_up(self, **kwargs):
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

        return "OK", ret

    @doc()
    @route("", methods=["PUT"])
    def modify(self):
        modify_user = ModifySchema().load(json.loads(request.data))
        user_service = UserService(modify_user)
        ret = user_service.modify()

        return ret

    @doc()
    @route("login", methods=["POST"])
    def log_in(self):
        login_user = LoginSchema().load(json.loads(request.data))
        if not login_user:
            return ("Not Founded User-info",
                    status.HTTP_204_NO_CONTENT)
        # 패스워드가 안맞는 경우는 unauthorized가 발생해야되긴 한데 ..
        user_service = UserService(login_user)
        tokens = user_service.log_in()

        return (tokens,
                status.HTTP_200_OK)

    @doc()
    @route("logout", methods=["GET"])
    def log_out(self):
        pass
