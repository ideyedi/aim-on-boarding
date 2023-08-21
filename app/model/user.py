import bcrypt
import mongoengine as me


class User(me.Document):
    user_id = me.StringField(required=True, max_length=100, unique=True)
    user_password = me.StringField(required=True, max_length=100)
    is_admin = me.BooleanField(default=False)

    def validate_pw(self, input_password):
        """
        Log-in 기능에서 패스워드 확인
        :param input_password: 로그인 시 요청으로 인입된 패스워드 값
        :return: Boolean
        """
        print(bcrypt.checkpw(input_password.encode("UTF-8"),
                             self.user_password.encode("UTF-8")))
        pass
