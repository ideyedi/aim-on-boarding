from flask import request, jsonify
from flask_api import status
from functools import wraps
from marshmallow import ValidationError

from app.schema.user import CreateSchema
import json


def user_info_validator(func):
    """
    Sign-up 전 인입된 User 정보를 확인
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            print(f"{__name__}{request.data}")
            CreateSchema().load(json.loads(request.data))

        except ValidationError as err:
            return jsonify(err.messages), status.HTTP_409_CONFLICT

        return func(*args, **kwargs)
    return decorated_view
