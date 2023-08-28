import jwt

from functools import wraps
from flask import request
from flask_api import status

from app.error import ApiError


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
    :param func:
    :return:
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)

    return decorator
