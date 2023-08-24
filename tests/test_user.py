import pytest
import logging
import bcrypt

from flask import url_for
from flask_api import status
from json import dumps

from tests.factories.user import UserFactory

logger = logging.getLogger("user-test")


class TestUserView:
    @pytest.fixture
    def fixture_user(self):
        return UserFactory.create()

    class TestHealthCheck:
        @pytest.fixture(autouse=True)
        def subject(self, client):
            url = url_for("route.UserView:healthcheck")
            return client.get(url)

        def test_endpoint_healthcheck(self, subject):
            assert status.HTTP_200_OK == subject.status_code

    class TestUserLogin:
        @pytest.fixture
        def post_form(self, fixture_user):
            return {
                "user_id": fixture_user.user_id,
                "user_password": bcrypt.hashpw(fixture_user.user_password.encode('utf-8'),
                                               bcrypt.gensalt()).decode('utf-8')
            }

        @pytest.fixture
        def subject(self, client, post_form):
            url = url_for("route.UserView:log_in")
            return client.post(url, data=dumps(post_form))

        def test_login(self, subject, fixture_user):
            """
            임의의 데이터를 이용한 로그인 시 실패되는 시나리오
            :param fixture_user: 난수 생성된 유저
            """
            # 난수로 생성된 아이디라 먼저 걸러지는 시나리오인데 hashcheck은 왜해
            logger.info(fixture_user.user_id)
            logger.info(fixture_user.user_password)
            logger.info(f"req status_code: {subject.status_code}")
            assert subject.status_code == status.HTTP_204_NO_CONTENT
