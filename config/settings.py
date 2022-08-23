import os
from dotenv import load_dotenv

from datetime import timedelta


load_dotenv()


DEBUG = True
LOG_LEVEL = 'DEBUG'
COMPOSE_HTTP_TIMEOUT = 180

SERVER_NAME = 'localhost:8000'
SECRET_KEY = os.getenv('SECRET_KEY')

# Flask-Mail.
MAIL_DEFAULT_SENDER = 'contact@local.host'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'flowstate.lims@gmail.com'
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

# Celery.
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5

# SQLAlchemy.
DB_URI = os.getenv('DB_URI')
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = os.getenv('SEED_ADMIN_PASSWORD')
REMEMBER_COOKIE_DURATION = timedelta(days=90)