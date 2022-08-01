import os

DEBUG = False

SERVER_NAME = 'localhost:8000'
SECRET_KEY = os.environ['SECRET_KEY']

MAIL_USERNAME = 'flowstate.lims@gmail.com'
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

DB_URI = os.environ['DB_URI']
SQLALCHEMY_DATABASE_URI = DB_URI

SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = os.environ['SEED_ADMIN_PASSWORD']