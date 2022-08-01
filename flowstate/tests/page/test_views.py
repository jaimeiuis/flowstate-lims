from flask import url_for

from lib.test import assert_status_with_message


class TestPage(object):
    def test_home_page(self, client):
        response = client.get(url_for('page.home'))
        assert response.status_code == 200