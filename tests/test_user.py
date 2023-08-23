import pytest

from tests.factories.user import UserFactory
from flask import url_for
from flask_api import status

from app.service.user import UserService

import logging
logger = logging.getLogger("user-test")


class TestUserView:
    @pytest.fixture
    def fixture_user(self):
        return UserFactory.create()

    @pytest.fixture(autouse=True)
    def subject(self, client):
        url = url_for("route.UserView:healthcheck")
        return client.get(url)

    class TestUserLogin:
        def test_endpoint_healthcheck(self, subject):
            # subject는 무슨 객체지..?
            assert status.HTTP_200_OK == subject.status_code

        def test_login(self, fixture_user):
            """
            임의의 데이터를 이용한 로그인 시 실패되는 시나리오
            :param fixture_user: 난수 생성된 유저
            """
            logger.info(fixture_user.user_password)
            service = UserService(fixture_user)
            logger.info(service.log_in())

            assert True
