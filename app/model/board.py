import mongoengine as me

from app.model.user import User


class Board(me.document):
    name = me.StringField()
    description = me.StringField()
    # 이러면 자료구조로 가지고 있고 추가적인 참조를 하지 않으려나
    admin = me.EmbeddedDocumentField(User)