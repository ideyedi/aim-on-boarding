import mongoengine as me


class User(me.Document):
    user_id = me.StringField(required=True, max_length=100, unique=True)
    user_password = me.StringField(required=True, max_length=100)
    is_admin = me.BooleanField(default=False)


class Authorization(me.Document):
    user_token = me.StringField(required=True)

    @classmethod
    def create(cls, user_id, is_admin):
        """
        일단 용도 파악이 우선
        :param user_id:
        :param is_admin:
        :return:
        """
        pass
