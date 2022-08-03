from flask import Flask
from celery import Celery
from itsdangerous import URLSafeTimedSerializer

from flowstate.blueprints.contact import contact
from flowstate.blueprints.page import page
from flowstate.blueprints.user import user
from flowstate.blueprints.user.models import User


from flowstate.extensions import (
    debug_toolbar,
    mail,
    csrf,
    db,
    login_manager
)


CELERY_TASK_LIST = [
    'flowstate.blueprints.contact.tasks',
]


def create_celery_app(app=None):
    """ Create Celery object, connect app/Celery configs, and connect tasks to app context. """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """ Create a Flask app. """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(contact)
    app.register_blueprint(page)
    app.register_blueprint(user)

    extensions(app)
    authentication(app, User)

    return app


def extensions(app):
    """ Mutate the Flask app with extensions. """
    debug_toolbar.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return None


def authentication(app, user_model):
    """ Initialize the Flask-Login extension (mutates the app passed in). """
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)

    @login_manager.token_loader
    def load_token(token):
        duration = app.config['REMEMBER_COOKIE_DURATION'].total_seconds()
        serializer = URLSafeTimedSerializer(app.secret_key)

        data = serializer.loads(token, max_age=duration)
        user_uid = data[0]

        return user_model.query.get(user_uid)