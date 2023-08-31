import pytest
import logging
import bcrypt

from flask import url_for
from flask_api import status
from json import dumps

from tests.factories.user import UserFactory

logger = logging.getLogger("user-test")


class DescribeUserFeature:
    @pytest.fixture
    def fixture_user(self):
        return UserFactory.create()

    @classmethod
    def success_check(cls, subject):
        assert subject.status_code == status.HTTP_200_OK

    class DescribeHealthCheck:
        @pytest.fixture(autouse=True)
        def subject(self, client):
            url = url_for("route.UserView:healthcheck")
            return client.get(url)

        def test_health_check(self):
            DescribeUserFeature.success_check()


def test_example():
    assert 1 == 1


    """
    class DescribeUserLogin:
        @pytest.fixture
        def post_form(self, fixture_user):
            eturn {
                "user_id": fixture_user.user_id,
                "user_password": bcrypt.hashpw(fixture_user.user_password.encode('utf-8'),
                                               bcrypt.gensalt()).decode('utf-8')
            }

        @pytest.fixture
        def subject(self, client, post_form):
            url = url_for("route.UserView:log_in")
            return client.post(url, data=dumps(post_form))

        def test_random_info_login_failed(self, subject, fixture_user):
            # 난수로 생성된 아이디라 먼저 걸러지는 시나리오인데 hashcheck은 왜해
            logger.info(fixture_user.user_id)
            logger.info(fixture_user.user_password)
            logger.info(f"req status_code: {subject.status_code}")
            assert subject.status_code == status.HTTP_204_NO_CONTENT
    """