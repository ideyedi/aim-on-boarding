import bcrypt

from typing import Dict, Any
from datetime import datetime, timedelta

from app.model.user import User
from core.user import *
from config import config as c


class UserService:
    def __init__(self, req: User):
        self.dao_user = req

    @classmethod
    def _create_access_token(cls, user_id: str, is_admin: bool, expire_time=None):
        if expire_time is not None:
            expire_time = datetime.utcnow() + expire_time
        else:
            expire_time = datetime.utcnow() + timedelta(minutes=c.ACCESS_TOKEN_EXPIRE_M)

        to_encode = {"user_id": user_id, "is_admin": is_admin, "expire": str(expire_time)}
        token = jwt.encode(to_encode, c.JWT_SECRET_KEY, c.ALGORITHM)

        return token

    @classmethod
    def _create_refresh_token(cls, user_id: str, is_admin: bool, expire_time=None):
        if expire_time is not None:
            expire_time = datetime.utcnow() + expire_time
        else:
            expire_time = datetime.utcnow() + timedelta(minutes=c.REFRESH_TOKEN_EXPIRE_M)

        to_encode = {"user_id": user_id, "is_admin": is_admin, "expire": str(expire_time)}
        token = jwt.encode(to_encode, c.JWT_REFRESH_SECRET_KEY, c.ALGORITHM)

        return token

    def sign_up(self):
        ret = self.dao_user.save()
        print(f"ret; {ret}")
        return status.HTTP_200_OK

    def log_in(self, input_pw):
        # invalid check 기능 위치 변경
        if not bcrypt.checkpw(input_pw.encode("UTF-8"),
                              self.dao_user.user_password.encode("UTF-8")):
            return False

        access_token = self._create_access_token(
            self.dao_user.user_id, self.dao_user.is_admin
        )
        refresh_token = self._create_access_token(
            self.dao_user.user_id, self.dao_user.is_admin
        )
        tokens_dict: Dict = {"access_token": access_token,
                             "refresh_token": refresh_token}

        return tokens_dict

    def modify(self, password: str = None, is_admin: bool = None):
        """
        user id 고정, password, is_admin 값 변경 가능
        변경되는 값이 있는 것만 바뀌게끔 구현하고 싶음
        :return:
        """
        print(f"{__name__}:{self.dao_user['user_id']}, {self.dao_user['user_password']}")
        print(f"{password}, {is_admin}")
        model_user = User(user_id=self.dao_user["user_id"])

        if password is not None:
            print("password changed")
            model_user.user_password = password

        if is_admin is not None:
            print("role changed")
            model_user.is_admin = is_admin

        model_user.save()

        return __name__

    def show_info(self):
        pass
