import bcrypt
import mongoengine as me


class User(me.Document):
    # MongoEngine Model에 직접 _id를 설정하게 되면
    # 개발자가 직접 컨트롤하는 것으로 인식해버림
    # 데이터를 쓸때 _id 값 Validation Failed 되어 버림
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

    def __repr__(self):
        return f"<User user_id={self.user_id}, is_admin={self.is_admin})>"
