from lib.mail import send_template_message
from flowstate.app import create_celery_app

celery = create_celery_app()


@celery.task()
def deliver_contact_email(email, message):
    ctx = {
        'email': email,
        'message': message
    }

    send_template_message(subject='[Flowstate] Contact',
                            sender=email,
                            recipients=[celery.conf.get('MAIL_USERNAME')],
                            reply_to=email,
                            template='contact/mail/index',
                            ctx=ctx)

    return None   