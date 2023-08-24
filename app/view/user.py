import json
import jwt

from flask import request, jsonify
from flask_apispec import marshal_with, doc, use_kwargs
from flask_classful import FlaskView, route
from flask_api import status

from app.service.user import user_info_validator, UserService
from app.schema.user import *
from app.error import ApiErrorSchema, ApiError


class UserView(FlaskView):
    """
    유저 Front side
    """
    @doc(summary="user apis heathCheck")
    @route("monitor", methods=["GET"])
    def healthcheck(self):
        print(f"{request.data}")
        return ("HeathCheck",
                status.HTTP_200_OK)

    shae = 2
    doc_string = f"{shae}, parameter 보이지 않는 문제 확인 필요"

    @route("", methods=["POST"])
    @doc(description=doc_string, summary="USER Feature 회원가입")
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

    @doc(summary="USER Feature 유저 정보 수정")
    @route("", methods=["PUT"])
    def modify(self):
        modify_user = ModifySchema().load(json.loads(request.data))
        user_service = UserService(modify_user)
        ret = user_service.modify()

        return ret

    @doc(summary="USER Feature 유저 정보 조회")
    @route("", methods=["GET"])
    @marshal_with(ApiErrorSchema, code=status.HTTP_400_BAD_REQUEST, description="test")
    @marshal_with(ApiErrorSchema, code=status.HTTP_500_INTERNAL_SERVER_ERROR, description="Server Error")
    @use_kwargs({"jwt_access_token": fields.String(required=True)}, location="headers")
    def get_info(self, jwt_access_token):
        """
        input : JWT
        JWT 파싱 후 user_id 기준으로 정보 조회
        location을 명시하면 custom header에 들어가는 걸 확인할 수 있음
        OAuth 2.0 Bearer Token Method
        : test token
        : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZXNqaUBnbWFpbC5jb20iLCJpc19hZG1pbiI6ZmFsc2UsImV4cGlyZSI6IjIwMjMtMDgtMjQgMDQ6Mzk6MTguMDMyOTgyIn0.te1hLM1zTswtgIge1FcwVaT2Nvx3vUgoXWxM8pEm--U
        """
        print(request.headers.get("jwt_access_token"))
        print(request.data, jwt_access_token)
        # values = request.headers.get("Authorization").split(" ")
        token = jwt_access_token
        bearer = jwt.decode(token,
                            key="access_secret",
                            algorithms="HS256")

        try:
            user_id = bearer["user_id"]
        except Exception as e:
            print(e.__str__())
            return ApiError("Not founed User-ID in token",
                            status_code=status.HTTP_406_NOT_ACCEPTABLE)

        #print(bearer, type(bearer))
        # token 체크 로직을 데코레이터로 빼자
        user_info = User.objects(user_id=user_id).get()
        #print(user_info.user_id)
        user_service = UserService(user_info)

        return ({"user_id": user_info.user_id,
                 "user_password": user_info.user_password,
                 "is_admin": user_info.is_admin},
                status.HTTP_200_OK
                )

    @doc(summary="USER Feature log-in")
    @route("login", methods=["POST"])
    def log_in(self):
        login_user = LoginSchema().load(json.loads(request.data))
        if not login_user:
            return ("Not Founded User-info",
                    status.HTTP_204_NO_CONTENT)

        try:
            input_password = json.loads(request.data)["user_password"]
        except KeyError:
            return ("Conflict password",
                    status.HTTP_401_UNAUTHORIZED)

        user_service = UserService(login_user)
        tokens = user_service.log_in(input_password)
        if not tokens:
            return ("Invalid password",
                    status.HTTP_401_UNAUTHORIZED)

        return (tokens,
                status.HTTP_200_OK)

    @doc()
    @route("logout", methods=["POST"])
    def log_out(self):
        pass
