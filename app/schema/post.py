from marshmallow import fields, Schema, post_load
from marshmallow import validates_schema, ValidationError

from app.model.post import Post
from app.model.board import Board


class PostSchema(Schema):
    __model__ = Post
    title = fields.Str(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class PostCreateSchema(Schema):
    """ creation input 용도로만 사용하는 serializer? """
    title = fields.Str(required=True)
    content = fields.Str()
    hashtag = fields.Str()
    board_title = fields.Str()
