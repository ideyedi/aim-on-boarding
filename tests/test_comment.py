import logging
import pytest

from flask import url_for

logger = logging.getLogger("test-comment")


class Describe_CommentFeature:

    class Describe_HealthCheck:
        @pytest.fixture
        def subject(self, client):
            url = url_for("route.CommentView:healthcheck")
            return client.get(url)

        def test_Comment_블루프린트_응답확인(self, subject):
            assert subject.status_code == 200
