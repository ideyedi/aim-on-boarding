import pytest

from flask import current_app
from config import DevelopConfig


class TestConfig:
    @pytest.fixture(scope="session")
    def fixture_app(self):
        from app import create_app

        app = create_app()
        return app

    @pytest.fixture(scope="function", autouse=True)
    def fixture_db(self):
        import mongoengine

        mongoengine.connect(host=DevelopConfig.mongo_url)
        # or sleep?
        yield
        mongoengine.disconnect()
