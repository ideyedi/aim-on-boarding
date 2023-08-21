import bcrypt

from flask import jsonify
from marshmallow import fields, Schema, post_load
from marshmallow import ValidationError, validates_schema
from flask_api import status

from app.model.user import User


class CreateSchema(Schema):
    user_id = fields.Str(required=True, unique=True)
    user_password = fields.Str(required=True)
    is_admin = fields.Boolean(default=False)

    @post_load
    def create_user(self, data, **kwargs):
        """
        유저 생성 시 패스워드 암호화
        :param data:
        :return:
        """
        print(f"{__name__}, create_user function start")
        if not User.objects(user_id=data["user_id"]):
            password = bcrypt.hashpw(
                data["user_password"].encode("UTF-8"),
                bcrypt.gensalt()
            ).decode("UTF-8")

            data["user_password"] = password
            return User(**data)

        return False

    @validates_schema
    def validate_create_user(self, data,  **kwargs):
        print(f"marshmallow validation check")
        pass


class LoginSchema(Schema):
    # 몽고가 관리하는 _id 값도 가지고 오고 싶은데.
    _id = fields.Str(unique=True)
    user_id = fields.Str(required=True, unique=True)
    user_password = fields.Str(required=True)

    @post_load
    def make_model(self, data, **kwargs):
        queryset_user = User.objects(user_id=data["user_id"])

        if not queryset_user:
            return False

        #print(queryset_user.first()["_id"])
        if not bcrypt.checkpw(data["user_password"].encode("UTF-8"),
                              queryset_user.first()["user_password"].encode("UTF-8")):
            # error handling을 좀더 graceful하게 정리했으면 ..
            return False

        return User(**data)

