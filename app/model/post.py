from mongoengine import *

from datetime import datetime

from app.model.board import Board
from app.model.user import User


class Author(EmbeddedDocument):
    user_id = StringField()

    def __repr__(self):
        return f"<Author user_id: {self.user_id}>"


class Post(Document):
    title = StringField(required=True)
    content = StringField()
    hashtag = StringField()

    create_time = DateTimeField(default=datetime.now().utcnow())
    modified_time = DateTimeField(default=datetime.now().utcnow())

    like = ListField(ReferenceField(User))
    author = EmbeddedDocumentField(Author)
    board = ReferenceField(Board)

    def __repr__(self):
        return f"<POST Model Title: {self.title}, like: {len(self.like)}>"
