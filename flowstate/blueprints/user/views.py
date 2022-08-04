from flask import (
    Blueprint,
    url_for,
    render_template,
    redirect,
    flash,
    request
)

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from lib.safe_next_url import safe_next_url

from flowstate.blueprints.user.forms import LoginForm, WelcomeForm
from flowstate.blueprints.user.models import User
from flowstate.blueprints.user.decorators import anonymous_required


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get('next'))

    if form.validate_on_submit():
        u = User.find_by_identity(request.form.get('identity'))

        if u and u.authenticated(password=request.form.get('password')):
            if login_user(u, remember=True) and u.is_active():
                u.update_activity_tracking(request.remote_addr)

                next_url = request.form.get('next')
                if next_url:
                    return redirect(safe_next_url(next_url))

                return redirect(url_for('user.settings'))
            else:
                flash('This account has been disabled.', 'error')
        else:
            flash('Identity or password is incorrect.', 'error')

    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.login'))


@user.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    if current_user.username:
        flash('You already picked a username.', 'warning')
        return redirect(url_for('user.settings'))

    form = WelcomeForm()

    if form.validate_on_submit():
        current_user.username = request.form.get('username')
        current_user.save()

        flash('Sign up is complete.', 'success')
        return redirect(url_for('user.settings'))

    return render_template('user/welcome.html', form=form)

@user.route('/settings')
@login_required
def settings():
    return render_template('user/settings.html')