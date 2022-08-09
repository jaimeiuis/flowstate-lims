from flask import Blueprint

from flask_login import login_required

from flowstate.blueprints.sample.forms import SearchForm
from flowstate.blueprints.sample.models import Sample


sample = Blueprint('sample', __name__, template_folder='templates')


@sample.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    pass