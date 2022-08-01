from flask import url_for

from lib.test import assert_status_with_message


class TestContact(object):
    def test_contact_page(self, client):
        response = client.get(url_for('contact.index'))
        assert response.status_code == 200

    def test_contact_form(self, client):
        form = {
            'email': 'foo@bar.com',
            'message': 'Test message'
        }
        
        response = client.post(url_for('contact.index'), data=form,
                                follow_redirects=True)
        assert_status_with_message(200, response, 'Thanks')