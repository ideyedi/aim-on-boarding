import json
import bcrypt

from marshmallow import fields, Schema, post_load
from marshmallow import validates_schema

from app.model.user import User


class UserSchema(Schema):
    user_id = fields.Str(required=True, unique=True)
    user_password = fields.Str(required=True)
    is_admin = fields.Boolean(default=False)


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
        #print(f"marshmallow validation check")
        pass


class LoginSchema(Schema):
    user_id = fields.Str(required=True, unique=True)
    user_password = fields.Str()

    @post_load
    def make_model(self, data, **kwargs):
        queryset_user = User.objects(user_id=data["user_id"])

        if not queryset_user:
            # 해당하는 id가 없을 경우 바로 Error return
            return False

        return queryset_user.first()


class ModifySchema(Schema):
    _id = fields.Dict()
    user_id = fields.Str(required=True, unique=True)
    user_password = fields.Str()
    is_admin = fields.Str()

    @post_load()
    def make_model(self, data, **kwargs):
        queryset_user = User.objects(user_id=data["user_id"])
        if not queryset_user:
            return False

        print(f"{queryset_user.first().to_json()}")
        user = json.loads(queryset_user.first().to_json())

        return User(**user)


class InfoSchema(UserSchema):
    expire = fields.DateTime()

    @post_load()
    def make_object(self, data, **kwargs):
        queryset = User.objects(user_id=data["user_id"])
        if not queryset:
            return False

        print(f"{__name__}/post_load")
        return User(**queryset.first())
