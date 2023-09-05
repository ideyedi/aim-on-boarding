import jwt
import json

from flask import request, jsonify
from flask_api import status
from marshmallow import ValidationError
from functools import wraps

from app.error import ApiError
from app.schema.user import CreateSchema


def check_access_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')

        if authorization_header and authorization_header.startswith('Bearer '):
            # Cut the "Bearer " prefix to get the token
            bearer_token = authorization_header[len('Bearer '):]
        else:
            return ApiError("Bearer token not found in Authorization header",
                            status_code=status.HTTP_401_UNAUTHORIZED)

        ret = jwt.decode(bearer_token, key="access_secret", algorithms="HS256")
        '''
        토큰 Expired 기능은 여기 추가하면 좋을듯
        '''

        kwargs = ret
        #print(f"{__bane__} : args:{args} \n kwargs: {kwargs}")
        return func(*args, **kwargs)

    return decorator


def check_refresh_token(func):
    """
    OAuth2.0 Refresh token Decorator
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)

    return decorator


def user_info_validator(func):
    """
    Sign-up 전 인입된 User 정보를 확인
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            CreateSchema().load(json.loads(request.data))

        except ValidationError as err:
            raise ApiError(f"{err.messages}",
                           status_code=status.HTTP_409_CONFLICT)

        return func(*args, **kwargs)
    return decorated_view
