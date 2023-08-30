from mongoengine import *


class Dashboard(Document):
    # 음 RFP만 봤을 땐 여긴 모델이 필요 없겠는데?
    # Schema를 이용한 처리만 하면 될듯?//
    def __repr__(self):
        return f"<DashBoard()>"
