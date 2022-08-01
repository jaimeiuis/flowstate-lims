import pytest

from config import settings
from flowstate.app import create_app


@pytest.yield_fixture(scope='session')
def app():
    """ Setup the Flask app and app context once for the testing session. """
    params = {
        'DEBUG': False,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
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