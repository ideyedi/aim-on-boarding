# pytest를 위한 공용 fixture 모음
import mongomock
import pytest
import mongoengine

from unittest import mock
from flask_mongoengine import MongoEngine
from flask import g

from config import DevelopConfig


@pytest.fixture(scope="session")
def app():
    from app import create_app
    import mongoengine
    app = create_app()

    mongoengine.disconnect(alias="Boarding")
    # Create_app에서 생성된 기능을 위한 DB Connection Close

    db = MongoEngine()
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": "on_board",
            "host": "localhost",
            "port": 27017,
            "mongo_client_class": mongomock.MongoClient
        }
    ]
    db.init_app(app)
    return app


@pytest.fixture(scope="function", autouse=True)
def get_test_db():
    mongoengine.connect('on_board',
                        host="localhost:27017",
                        mongo_client_class=mongomock.MongoClient,
                        alias="testdb")
    yield
    mongoengine.disconnect(alias="testdb")


@pytest.fixture()
def client(app):
    client = app.test_client()
    db = mongoengine
    return client

