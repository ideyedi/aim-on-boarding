import mongoengine as me

from datetime import datetime

from app.model.board import Board
from app.model.user import User


class Author(me.EmbeddedDocument):
    user_id = me.StringField()

    def __repr__(self):
        return f"<Author user_id: {self.user_id}>"


class Post(me.Document):
    title = me.StringField(required=True)
    content = me.StringField()
    hashtag = me.StringField()

    create_time = me.DateTimeField(default=datetime.now().utcnow())
    modified_time = me.DateTimeField(default=datetime.now().utcnow())
    # 단순히 integer만 관리할 경우 내가 누른 좋아요 판단이 불가능
    # linking 구조로 변경
    like = me.ListField(me.ReferenceField(User))
    author = me.EmbeddedDocumentField(Author)
    board = me.ReferenceField(Board)

    def __repr__(self):
        return f"<POST Model Title: {self.title}, modified T: {self.modified_time}>"
