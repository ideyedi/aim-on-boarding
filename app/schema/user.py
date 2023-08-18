import bcrypt

from marshmallow import fields, Schema, post_load, validates_schema
from app.model.user import User


class CreateSchema(Schema):
    user_id = fields.Str(required=True, unique=True)
    user_password = fields.Str(required=True)
    is_admin = fields.Boolean(default=False)

    @post_load
    def create_user(self, data, **kwargs):
        """
        유저 생성 시 패스워드 암호화 로직
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
            user = User(**data)
            return user

        return False

    @validates_schema
    def validate_create_user(self, data,  **kwargs):
        print(f"D: {data}")
        pass


class InfoSchema(Schema):
    pass
