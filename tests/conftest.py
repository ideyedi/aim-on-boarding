# pytest를 위한 공용 fixture 모음
import mongomock
import pytest
import mongoengine

from unittest import mock
from config import DevelopConfig


def create_mock_session():
    session = mock.Mock()
    session.in_transaction = False

    def _start_transaction():
        session.in_transaction = True

    def _end_session():
        session.in_transaction = False

    session.start_transaction = _start_transaction
    session.end_session = _end_session
    return session


@pytest.fixture(scope="session")
def app():
    from app import create_app
    app = create_app()
    return app


@pytest.fixture()
def client(app):
    client = app.test_client()
    return client


@pytest.fixture(scope="function", autouse=True)
def get_db():
    mongoengine.connect('on_board',
                        host=DevelopConfig.mongo_url,
                        mongo_client_class=mongomock.MongoClient,
                        alias="testdb")
    with mock.patch.object(attribute="what is this", side_effect=create_mock_session):
        yield

    mongoengine.disconnect(alias="testdb")