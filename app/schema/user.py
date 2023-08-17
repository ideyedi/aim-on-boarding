import bcrypt

from marshmallow import fields, Schema, post_load, validates_schema
from app.model.user import User


class CreateSchema(Schema):
    user_id = fields.Str(required=True, unique=True)
    user_password = fields.Str(required=True)
    is_admin = fields.Boolean(default=False)

    @post_load
    def create_user(self):
        pass

    @validates_schema
    def validate_create_user(self, data,  **kwargs):
        print(f"D: {data}")
        pass


class InfoSchema(Schema):
    pass
