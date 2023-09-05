import pytest
import logging
import requests

from flask import url_for

from tests.factories.user import *
from app.service.user import UserService

logger = logging.getLogger("test-user")


class Describe_UserFeature:

    class Describe_HealthCheck:
        @pytest.fixture(autouse=True)
        def subject(self, client):
            url = url_for("route.UserView:healthcheck")
            return client.get(url)

        def test_User_블루프린트_응답확인(self, subject):
            a = 1
            # test
            assert a == 1
            assert subject.status_code == 200

    class Describe_POST_Sign_up:

        class Context_아이디_패스워드_입력_상황:
            @pytest.fixture
            def fixture_user(self):
                return UserFactory.create()

            @pytest.fixture
            def no_email_user(self):
                return UserNoEmailFactory.create()

            def test_이메일_아이디_가입_201(self, fixture_user):
                user_service = UserService(fixture_user)
                ret = user_service.sign_up()
                logger.info(f"return value {ret}")
                assert ret == 201

            def test_이메일이_아닌_아이디_가입_201(self, no_email_user):
                user_service = UserService(no_email_user)
                ret = user_service.sign_up()
                logger.info(f"return value {ret}")
                assert ret == 201

        class Context_중복된_아이디가_존재:
            @pytest.fixture
            def static_user(self):
                return UserStaticFactory.create()

            @pytest.fixture
            def subject(self, client):
                url = url_for("route.UserView:sign_up")
                return client.get(url)

            def test_중복된_아이디가_존재하여_실패_409(self, static_user, client):
                logger.info(static_user.user_id)
                # dummy data input
                user_service = UserService(static_user)
                user_service.sign_up()

                data = {"user_id": static_user.user_id, "user_password": static_user.user_password}
                headers = {
                    "context-type": "application/json"
                }

                with requests.Session() as sess:
                    response = sess.post("http://localhost:5000/user", headers=headers, json=data, verify=False)

                assert response.status_code == 409
