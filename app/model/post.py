import mongoengine as me

from app.model.user import User
from app.model.board import Board


class Post(me.Document):
    title = me.StringField()
    content = me.StringField()
    hashtag = me.StringField()
    create_time = me.DateTimeField()
    delete_time = me.DateTimeField()
    like = me.IntField()
    # User id reference, FK 역할
    # mongo _id 필드를 가지고 사용할 수 있나?
    user_id = me.ReferenceField(User)
    board = me.EmbeddedDocumentField(Board)

