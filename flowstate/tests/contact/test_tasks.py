from flowstate.extensions import mail
from flowstate.blueprints.contact.tasks import deliver_contact_email


class TestContact(object):
    def test_deliver_support_email(self, client):
        form = {
            'email': 'foo@bar.com',
            'message': 'Test message'
        }

        with mail.record_messages() as outbox:
            deliver_contact_email(form.get('email'), form.get('message'))

            assert len(outbox) == 1
            assert form.get('email') in outbox[0].body