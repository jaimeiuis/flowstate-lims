import pytest

from config import settings
from flowstate.app import create_app
from flowstate.extensions import db as _db
from flowstate.blueprints.user.models import User


@pytest.yield_fixture(scope='session')
def app():
    """ Setup the Flask app and app context once for the testing session. """
    db_uri = '{0}_test'.format(settings.SQLALCHEMY_DATABASE_URI)
    params = {
        'DEBUG': False,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': db_uri
    }

    _app = create_app(settings_override=params)

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """ Setup an app client once for each test function. """
    yield app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """ Setup the database once for the testing session. """
    _db.drop_all()
    _db.create_all()

    params = {
        'role': 'admin',
        'email': 'admin@local.host',
        'password': 'password'
    }

    admin = User(**params)

    _db.session.add(admin)
    _db.session.commit()

    return _db


@pytest.yield_fixture(scope='function')
def session(db):
    """Use rollbacks and nested sessions for fast tests. """
    db.session.begin_nested()

    yield db.session

    db.session.rollback()


@pytest.fixture(scope='function')
def users(db):
    """ Set up user fixtures once per test. """
    db.session.query(User).delete()

    users = [
        {
            'role': 'admin',
            'email': 'admin@local.host',
            'password': 'password'
        },
        {
            'active': False,
            'email': 'disabled@local.host',
            'password': 'password'
        }
    ]

    for user in users:
        db.session.add(User(**user))

    db.session.commit()

    return db