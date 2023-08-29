from mongoengine import *


class Dashboard(Document):

    def __repr__(self):
        return f"<DashBoard()>"
