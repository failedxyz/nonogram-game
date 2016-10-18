import pytest

from app import app as nonogram_app
from config import Config as AppConfig
from models import db as nonogram_db


@pytest.fixture(scope="session")
def app(request):
    app = nonogram_app
    app.config.from_object(AppConfig(testing=True))
    app.config["TESTING"] = True

    ctx = app.test_request_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="class")
def db(request, app):
    nonogram_db.reflect()
    nonogram_db.create_all()

    def teardown():
        nonogram_db.session.close_all()
        nonogram_db.reflect()

    request.addfinalizer(teardown)
    return nonogram_db


@pytest.fixture(scope="class")
def session(request, db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
