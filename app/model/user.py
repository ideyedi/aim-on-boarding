import mongoengine as me
import datetime
import jwt
from flask import current_app


class User(me.Document):
    """
    User ID 이외에 unique key로 uuid를 적용해보는게..?
    """
    # uuid, MongoDB에서 기본적으로 Hash Key를 생성, 관리하기 때문에 굳이 필요 없음
    user_id = me.StringField(required=True, max_length=100, unique=True)
    user_password = me.StringField(required=True, max_length=100)
    is_admin = me.BooleanField(default=False)


class Authorization(me.Document):
    user_token = me.StringField(required=True)

    @classmethod
    def create(cls, user_id, is_admin):
        """
        일단 용도 파악이 우선
        :param user_id:
        :param is_admin:
        :return:
        """
        pass
