from flask import (
    Blueprint,
    render_template
)

from flask_login import login_required

from flowstate.blueprints.sample.forms import SearchForm
from flowstate.blueprints.sample.models import Sample, Dashboard


sample = Blueprint('sample', __name__, template_folder='templates')


@sample.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    group_and_count_samples = Dashboard.group_and_count_samples()

    return render_template('sample/page/dashboard.html',
                            group_and_count_samples=group_and_count_samples)