from flask import (
    Blueprint,
    url_for,
    render_template,
    redirect,
    flash,
    request
)

from flask_login import (
    login_required,
    login_user,
    logout_user
)

from flowstate.blueprints.user.forms import LoginForm
from flowstate.blueprints.user.models import User
from flowstate.blueprints.user.decorators import anonymous_required


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get('next'))

    if form.validate_on_submit():
        pass

    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.login'))