import os
from dotenv import load_dotenv


load_dotenv()


DEBUG = False

SERVER_NAME = 'localhost:8000'
SECRET_KEY = os.getenv('SECRET_KEY')

MAIL_USERNAME = 'flowstate.lims@gmail.com'
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

DB_URI = os.getenv('DB_URI')
SQLALCHEMY_DATABASE_URI = DB_URI

SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = os.getenv('SEED_ADMIN_PASSWORD')