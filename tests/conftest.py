# pytest를 위한 공용 fixture 모음
import pytest
import mongomock

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


@pytest.fixture()
def mock_mongo_client():
    # mongomock을 이용하여 가상의 MongoDB 클라이언트를 생성합니다.
    return mongomock.MongoClient()
