import json
import jwt

from flask import request, jsonify
from flask_api import status
from functools import wraps
from marshmallow import ValidationError
from typing import Dict, Any
from datetime import datetime, timedelta

from app.schema.user import CreateSchema
from app.model.user import User
from config import config as c


def user_info_validator(func):
    """
    Sign-up 전 인입된 User 정보를 확인
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            CreateSchema().load(json.loads(request.data))

        except ValidationError as err:
            return jsonify(err.messages), status.HTTP_409_CONFLICT

        return func(*args, **kwargs)
    return decorated_view


class UserService:
    def __init__(self, req: Dict[str, Any]):
        self.dao_user = req
        print(self.dao_user["user_id"])

    @classmethod
    def _create_access_token(cls, user_id: str, is_admin: bool, expire_time=None):
        if expire_time is not None:
            expire_time = datetime.utcnow() + expire_time
        else:
            expire_time = datetime.utcnow() + timedelta(minutes=c.ACCESS_TOKEN_EXPIRE_M)

        to_encode = {"user_id": user_id, "is_admin": is_admin, "expire": str(expire_time)}
        token = jwt.encode(to_encode, c.JWT_SECRET_KEY, c.ALGORITHM)

        return token

    @classmethod
    def _create_refresh_token(cls, user_id: str, is_admin: bool, expire_time=None):
        if expire_time is not None:
            expire_time = datetime.utcnow() + expire_time
        else:
            expire_time = datetime.utcnow() + timedelta(minutes=c.REFRESH_TOKEN_EXPIRE_M)

        to_encode = {"user_id": user_id, "is_admin": is_admin, "expire": str(expire_time)}
        token = jwt.encode(to_encode, c.JWT_REFRESH_SECRET_KEY, c.ALGORITHM)

        return token

    def sign_up(self):
        model_user = User(user_id=self.dao_user["user_id"],
                          user_password=self.dao_user["user_password"],
                          is_admin=self.dao_user["is_admin"])
        ret = model_user.save()
        print(ret)
        return status.HTTP_200_OK

    def log_in(self):
        access_token = self._create_access_token(
            self.dao_user["user_id"], self.dao_user["is_admin"]
        )

        refresh_token = self._create_access_token(
            self.dao_user["user_id"], self.dao_user["is_admin"]
        )
        tokens_dict: Dict = {"access_token": access_token,
                             "refresh_token": refresh_token}

        return jsonify(tokens_dict)
