import mongoengine as me


class EmbedUser(me.EmbeddedDocument):
    user_id = me.StringField(required=True)


class Board(me.Document):
    board_name = me.StringField(required=True, max_length=100)
    description = me.StringField(max_length=500)
    admin = me.EmbeddedDocumentField(EmbedUser)

    def __repr__(self):
        return f"<Board(name={self.board_name}, desc={self.description})>"
