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
    """ 포스트 생성 값 입력을 위한 Serializer/Schema """
    title = fields.Str(required=True)
    content = fields.Str()
    hashtag = fields.Str()
    board_title = fields.Str()


class PostInfoSchema(PostSchema):
    content = fields.Str()
    hashtag = fields.Str()
    post_id = fields.Str(default=None)

    @post_load()
    def make_object(self, data, **kwargs):
        #print(data)
        #print(kwargs.get("post_id"))
        post_idx = data.pop("post_id")
        #print(post_idx, data)
        return self.__model__(**data), post_idx
