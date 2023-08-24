import json

from marshmallow import fields, Schema
from marshmallow import validates_schema

from app.model.board import Board


class BoardSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    admin = fields.Str(required=True)


class BoardCreateSchema(BoardSchema):

    @validates_schema
    def validate_creation(self):
        print("{__name__}")
        pass
