from mongoengine import *


class EmbedUser(EmbeddedDocument):
    user_id = StringField(required=True)


class Board(Document):
    board_name = StringField(required=True, max_length=100)
    description = StringField(max_length=500)
    admin = EmbeddedDocumentField(EmbedUser)

    def __repr__(self):
        return f"<Board(name={self.board_name}, desc={self.description})>"
