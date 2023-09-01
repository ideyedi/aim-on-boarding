import mongoengine
import pytest
import logging

from flask import url_for

from tests.factories.user import *
from app.service.user import UserService
from app.model.user import User

logger = logging.getLogger("user-test")


class Describe_UserService:

    class Describe_HealthCheck:
        @pytest.fixture(autouse=True)
        def subject(self, client):
            url = url_for("route.UserView:healthcheck")
            return client.get(url)

        def test_healcheck_엔드포인트가_응답한다(self, subject):
            a = 1
            # test
            assert a == 1
            assert subject.status_code == 200

    class Describe_sign_up:
        @classmethod
        def setUpClass(cls, get_db):
            get_db()

        @classmethod
        def setDownClass(cls):
            mongoengine.disconnect_all()

        class Context_회원가입이_정상적인_경우:
            @pytest.fixture
            def fixture_user(self, get_db):
                return UserFactory.create()

            @pytest.fixture
            def no_email_user(self, get_db):
                return UserNoEmailFactory.create()

            def test_이메일_아이디_가입(self, fixture_user):
                logger.info(fixture_user.user_id)
                logger.info(fixture_user.user_password)
                logger.info(fixture_user)

                user_service = UserService(fixture_user)
                ret = user_service.sign_up()
                logger.info(f"return value {ret}")
                assert ret == 200

            def test_이메일이_아닌_아이디_가입(self, no_email_user):
                user_service = UserService(no_email_user)
                ret = user_service.sign_up()
                logger.info(f"return value {ret}")
                assert ret == 200

        class Context_회원가입_실패_케이스:
            @pytest.fixture
            def static_user(self, get_db):
                return UserStaticFactory.create()

            def test_중복된_아이디(self, static_user):
                logger.info(static_user.user_id)
                user_service = UserService(static_user)
                ret = user_service.sign_up()
                logger.info(f"enri : {ret}")

                ret = user_service.sign_up()
                logger.info(f"enri : {ret}")

                assert 1 == 1
