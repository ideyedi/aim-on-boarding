from mongoengine import *

from enum import Enum
from datetime import datetime
from app.model.post import Post


class ParentType(Enum):
    post = "post"
    comment = "comment"


class Comment(Document):
    content = StringField()
    # Parent_type를 설정하여 구분되어있는 document를 한번에 알수 있게끔 처리
    # 근데 Rank가 0이면 바로 그냥 댓글인 걸 알수 있긴 하네
    # 해당 Comment가 속한
    involve = StringField(required=True)
    # 바로 상위 객체 id : Post일 수도, Comment일 수도 있음
    # 아 이거 굳이 필요 없을지도. 랭크로 정렬하면 되네
    parent = StringField(required=True)
    # 이건 필요한지 고민 필요
    parent_type = EnumField(default=ParentType.post, enum=ParentType)
    rank = IntField(default=0)
    # JWT User 정보
    author = StringField()
    create_time = DateTimeField(default=datetime.now().utcnow())

