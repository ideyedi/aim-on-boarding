from mongoengine import *

from enum import Enum
from app.model.post import Post


class ParentType(Enum):
    post = 0
    comment = 1


class Comment(Document):
    content = StringField()
    # Parent_type를 설정하여 구분되어있는 document를 한번에 알수 있게끔 처리
    # 근데 Rank가 0이면 바로 그냥 댓글인걸 알수 있긴 하네
    parent = ReferenceField(Post)
    parent_type = IntField(default=0)
    rank = IntField(default=0)
    # ㅋㅋㅋ Post 쪽에 작성자에는 뭐 좀 더 넣을까
    author = StringField()
