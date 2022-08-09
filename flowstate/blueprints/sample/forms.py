from flask_wtf import Form

from wtforms import StringField
from wtforms.validators import Length, Optional


class SearchForm(Form):
    q = StringField('Search terms', [Optional(), Length(1, 256)])


