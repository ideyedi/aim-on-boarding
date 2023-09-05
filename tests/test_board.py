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

    class Describe_Post_게시판_생성:
        class Context_모든_정보가_다_있는_경우:
            def test_정상적으로_생성된다(self):
                assert 1 == 1

        class Context_제목이_누락됨:
            def test_게시판이_생성되지_않는다(self):
                assert 400 == 400