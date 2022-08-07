from flask import url_for

from lib.test import assert_status_with_message, ViewTestMixin
from flowstate.blueprints.user.models import User


class TestLogin(ViewTestMixin):
    def test_login_page(self):
        """ Successfully render the login page. """
        response = self.client.get(url_for('user.login'))
        assert response.status_code == 200

    def test_login(self):
        """ Login successfully. """
        response = self.login()
        assert response.status_code == 200

    def test_login_disable(self):
        """ Fail to login due to disabled account. """
        response = self.login(identity='disabled@local.host')

        assert_status_with_message(200, response,
                                    'This account has been disabled.')
        
    def test_login_fail(self):
        """ Fail to login due to invalid login credentials. """
        response = self.login(identity='foo@bar.com')
        assert_status_with_message(200, response,
                                    'Identity or password is incorrect.')

    def test_logout(self):
        """ Logout successfully. """
        self.login()

        response = self.logout()
        assert_status_with_message(200, response,
                                    'You have been logged out.')


class TestSignup(ViewTestMixin):
    def test_signup_page(self):
        """ Successfully render the signup page. """
        response = self.client.get(url_for('user.signup'))

        assert response.status_code == 200

    def test_welcome_page(self, users):
        """ Successfully render the welcome page. """
        self.login()
        response = self.client.get(url_for('user.welcome'))

        assert response.status_code == 200

    def test_begin_signup_fail_logged_in(self, users):
        """ If logged in, signup should redirect to settings. """
        self.login()
        response = self.client.get(url_for('user.signup'),
                                    follow_redirects=False)

        assert response.status_code == 302

    def test_begin_signup_fail(self):
        """ Fail to signup if using an existing account. """
        user = {
            'email': 'admin@local.host',
            'password': 'password'
        }

        response = self.client.post(url_for('user.signup'), data=user,
                                    follow_redirects=True)

        assert_status_with_message(200, response, 'Already exists.')

    def test_signup(self, users):
        """ Successfully sign up. """

        user = {
            'email': 'new@local.host',
            'password': 'password'
        }

        response = self.client.post(url_for('user.signup'), data=user,
                                    follow_redirects=True)

        assert response.status_code == 200

    def test_welcome(self, users):
        """ Successfully create a username. """
        self.login()

        user = {
            'username': 'nocapfrfr'
        }

        response = self.client.post(url_for('user.welcome'), data=user,
                                    follow_redirects=True)

        assert response.status_code == 200

    def test_welcome_with_existing_username(self, users):
        """ Fail to create username if it already exists. """
        self.login()

        u = User.find_by_identity('admin@local.host')
        u.username = 'nocapfrfr'
        u.save()

        user = {
            'username': 'nocapfrfr'
        }

        response = self.client.post(url_for('user.welcome'), data=user,
                                    follow_redirects=True)

        assert_status_with_message(200, response,
                                    'You already picked a username.')


class TestSettings(ViewTestMixin):
    def test_settings_page(self):
        """ Settings renders successfully. """
        self.login()
        response = self.client.get(url_for('user.settings'))

        assert response.status_code == 200
