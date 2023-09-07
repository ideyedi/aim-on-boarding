import jwt

from flask import request
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
    @doc(tags=["User"], summary="user apis heathCheck")
    @route("monitor", methods=["GET"])
    def healthcheck(self):
        print(f"{request.data}")
        return ("HeathCheck",
                status.HTTP_200_OK)

    @route("", methods=["POST"])
    @doc(tags=["User"], description="user sign-up", summary="USER Feature 회원가입")
    @user_info_validator
    @use_kwargs(UserSchema, location="json")
    def sign_up(self, **kwargs):
        user = CreateSchema().load(json.loads(request.data))
        if user is False:
            return "Failed Sign-up", status.HTTP_409_CONFLICT

        user_service = UserService(user)
        ret = user_service.sign_up()
        if not ret:
            raise ApiError("Not Acceptable",
                           status_code=status.HTTP_406_NOT_ACCEPTABLE)

        return ("Sign-up Success",
                status.HTTP_201_CREATED)

    @doc(tags=["User"], summary="USER Feature 유저 정보 수정")
    @route("", methods=["PUT"])
    def modify(self):
        modify_user = ModifySchema().load(json.loads(request.data))
        user_service = UserService(modify_user)
        ret = user_service.modify()

        return ret

    @doc(tags=["User"], summary="USER Feature 유저 정보 조회")
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
        """
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

    @doc(tags=["User"], summary="USER Feature log-in")
    @route("login", methods=["POST"])
    @use_kwargs(LoginSchema, location="json", apply=False)
    def log_in(self):
        login_user = LoginSchema().load(json.loads(request.data))
        if not login_user:
            raise ApiError("Not Founded User-info",
                           status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            input_password = json.loads(request.data)["user_password"]
        except Exception as e:
            raise ApiError(f"{e}",
                           status_code=status.HTTP_401_UNAUTHORIZED)

        user_service = UserService(login_user)
        tokens = user_service.log_in(input_password)
        if not tokens:
            raise ApiError("Invalid password",
                           status_code=status.HTTP_401_UNAUTHORIZED)

        return (tokens,
                status.HTTP_200_OK)

    @doc(tags=["User"], summary="-")
    @route("logout", methods=["POST"])
    def log_out(self):
        pass
