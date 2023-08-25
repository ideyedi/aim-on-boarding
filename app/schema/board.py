from marshmallow import fields, Schema, post_load
from marshmallow import validates_schema, ValidationError

from app.model.board import Board


class BoardSchema(Schema):
    __model__ = Board
    board_name = fields.Str(required=True)
    description = fields.Str()

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class BoardCreateSchema(BoardSchema):
    admin = fields.Str(default="admin")

    @validates_schema
    def validate_create(self, data, **kwargs):
        # location 'query' 일 경우 self.context
        # location이 'json_or_form' 일 경우 ??
        # apply=False인 경우 schema validata를 하지 않네..
        print(self.context)
        print(f"{__name__}, Data: {data}")
        pass


class BoardDeleteSchema(BoardSchema):
    id = fields.String(attribute="_id")

    @validates_schema
    def validate_delete(self, data, **kwargs):
        if id is 0:
            raise ValidationError("Not Founded board-id")


class BoardInfoSchema(BoardSchema):
    admin = fields.Str(required=True)

    @validates_schema
    def validate_info(self, data, **kwargs):
        print(f"{self.__name__}")
        pass

