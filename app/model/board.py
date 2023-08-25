import mongoengine as me


class EmbedUser(me.EmbeddedDocument):
    _id = me.DictField()
    user_id = me.StringField(required=True)


class Board(me.Document):
    _id = me.DictField()
    board_name = me.StringField(required=True, max_length=100)
    description = me.StringField(max_length=500)
    admin = me.EmbeddedDocumentField(EmbedUser)

    def __repr__(self):
        return f"<Board(_id={self._id}\r name={self.board_name}\r desc={self.description})>"
