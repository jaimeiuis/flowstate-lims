from flask import (
    Blueprint,
    render_template,
    flash,
    url_for,
    request,
    redirect
)

from flowstate.blueprints.contact.forms import ContactForm


contact = Blueprint('contact', __name__, template_folder='templates')


@contact.route('/contact', methods=['GET', 'POST'])
def index():
    """ Following ContactForm submission, send a contact email. """
    form = ContactForm()

    if form.validate_on_submit():
        from flowstate.blueprints.contact.tasks import deliver_contact_email

        deliver_contact_email.delay(request.form.get('email'),
                                    request.form.get('message'))

        flash('Thanks, we will respond to your inquiry shortly', 'success')
        return redirect(url_for('contact.index'))

    return render_template('contact/index.html', form=form)