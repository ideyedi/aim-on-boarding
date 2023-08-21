import json

from flask import request, jsonify
from flask_api import status
from functools import wraps
from marshmallow import ValidationError
from typing import Dict, Any

from app.schema.user import CreateSchema
from app.model.user import User


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

    def sign_up(self):
        model_user = User(user_id=self.dao_user["user_id"],
                          user_password=self.dao_user["user_password"],
                          is_admin=self.dao_user["is_admin"])
        #ret = model_user.save()
        #print(ret)
        pass

    @classmethod
    def log_in(cls):
        pass
