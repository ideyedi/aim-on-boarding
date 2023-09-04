import logging
import pytest

from flask import url_for

logger = logging.getLogger("test-board")


class Describe_BoardFeature:

    class Describe_HealthCheck:
        @pytest.fixture
        def subject(self, client):
            url = url_for("route.BoardView:healthcheck")
            return client.get(url)

        def test_board_블루프린트_응답확인(self, subject):
            assert subject.status_code == 200

    class Describe_CreationBoard:
        class Context_게시판_생성:
            pass
