from collections import OrderedDict

from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer

from flask import current_app

from flask_login import UserMixin

from lib.util_sqlalchemy import ResourceMixin
from flowstate.extensions import db


class User(UserMixin, ResourceMixin, db.Model):
    ROLE = OrderedDict([
        ('member', 'Member'),
        ('admin', 'Admin')
    ])

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # Authentication
    role = db.Column(db.Enum(*ROLE, name='role_types', native_enum=False),
                        index=True, nullable=False, server_default='member')
    active = db.Column('is_active', db.Boolean(), nullable=False,
                        server_default='1')
    username = db.Column(db.String(24), unique=True, index=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False,
                        server_default='')
    password = db.Column(db.String(128), nullable=False, server_default='')

    # Activity tracking
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_ip = db.Column(db.String(45))

    def __init__(self, **kwargs):
        """ Call Flask-SQLAlchemy's constructor. """
        super(User, self).__init__(**kwargs)

        self.password = User.encrypt_password(kwargs.get('password', ''))

    @classmethod
    def find_by_identity(cls, identity):
        """ Find a user via email or username. """
        return User.query.filter(
            (User.email == identity) | (User.username == identity)).first()

    @classmethod
    def encrypt_password(cls, plaintext_password):
        """ Hash a plaintext password. """
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None

    def is_active(self):
        """ Check if a user is active. """
        return self.active

    def authenticated(self, with_password=True, password=''):
        """ Check if a user/password is authenticated. """
        if with_password:
            return check_password_hash(self.password, password)

        return True

    def update_activity_tracking(self, ip_address):
        """ Update various fields of a User. """
        self.sign_in_count += 1

        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_sign_in_ip = ip_address

        return self.save()

    def get_auth_token(self):
        """ Satisfies Flask-Login's requirement for a user's auth token. """
        private_key = current_app.config['SECRET_KEY']

        serializer = URLSafeTimedSerializer(private_key)
        data = [str(self.id), md5(self.password.encode('utf-8')).hexdigest()]

        return serializer.dumps(data)
