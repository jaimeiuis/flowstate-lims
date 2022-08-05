from flask_wtf import Form
from wtforms import HiddenField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms_components import Unique, EmailField, Email

from flowstate.blueprints.user.models import User, db


class LoginForm(Form):
    next = HiddenField()
    identity = StringField('Username or email',
                           [DataRequired(), Length(3, 254)])
    password = PasswordField('Password', [DataRequired(), Length(8, 128)])


class SignupForm(Form):
    email = EmailField(validators=[
        DataRequired(),
        Email(),
        Unique(
            User.email,
            get_session=lambda: db.session
        )
    ])
    password = PasswordField('Password', [DataRequired(), Length(8, 128)])


class WelcomeForm(Form):
    username_message = 'Letters, numbers, and underscores only.'

    username = StringField(validators=[
        Unique(
            User.username,
            get_session=lambda: db.session
        ),
        DataRequired(),
        Length(1, 16),
        Regexp(r'^\w+$', message=username_message)
    ])