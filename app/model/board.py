import mongoengine as me

from app.model.user import User


class Board(me.document):
    _id = me.Document
    name = me.StringField(required=True)
    description = me.StringField(max_length=500)
    admin = me.EmbeddedDocumentField(User.user_id)

    def __repr__(self):
        return f"<Board(_id={self._id}\r name={self.name}\r desc={self.description})>"
