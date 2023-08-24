from functools import wraps
from flask_apispec import doc


def check_access_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        #print(f"{args}")
        #print(**kwargs)
        return func(*args, **kwargs)

    #doc(params={"Authorization": {"in": "header", "type": "string", "required": True,
    #                              "default": "access_token"}})(func)
    return decorator
