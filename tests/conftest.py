# pytest를 위한 공용 fixture 모음
import pytest

from flask import current_app
from config import DevelopConfig


@pytest.fixture(scope="session")
def app():
    from app import create_app

    app = create_app()
    return app


@pytest.fixture()
def fixture_client(fixture_app):
    client = fixture_app.test_client()
    return client


@pytest.fixture(scope="function", autouse=True)
def db(app):
    import mongoengine

    mongoengine.connect(host=DevelopConfig.mongo_url)
    # or sleep?
    yield
    mongoengine.disconnect()
