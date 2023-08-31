from marshmallow import Schema, fields, post_load
from marshmallow import validates_schema, ValidationError

from app.model.comment import Comment


# FastAPI의 Pydantic 역할을 marshmallow가 해주고 있음
class CommentSchema(Schema):
    __model__ = Comment
    content = fields.Str(required=True)
    involve = fields.Str(required=True)
    parent = fields.Str(required=True)
    # 0일 경우 댓글, 0 이상일 경우 대댓글
    rank = fields.Int(default=0)

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class CommentCreateSchema(CommentSchema):
    pass


class CommentInfoSchema(CommentSchema):
    id = fields.Str()
    author = fields.Str(required=True)
    parent_type = fields.Str()
