import unittest

from flask.ext.login import current_user
from flask import request

from base import BaseTestCase
from project import bcrypt
from project.models import User


class UsersViewsTests(BaseTestCase):

    # check login page loads
    def test_login_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertIn('Please login', response.data)

    # check login works with correct credentials
    def test_login_works_with_correct_creds(self):
        # need to keep the test client context around otherwise the context
        # object get cleaned up after we're logged in and we need to access
        # the current_user for our test
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username='admin', password='admin'),
                follow_redirects=True)
            self.assertIn('You were just logged in', response.data)
            self.assertTrue(current_user.name == "admin")
            self.assertTrue(current_user.is_active())

    # check login does not work with incorrect credentials
    def test_login_does_not_work_with_incorrect_creds(self):
        response = self.client.post(
            '/login',
            data=dict(username='notadmin', password='notadmin'),
            follow_redirects=True)
        self.assertIn('Invalid credentials, Please try again.', response.data)

    # check logout works
    def test_logout_works(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username='admin', password='admin'),
                follow_redirects=True)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn('You were just logged out', response.data)
            self.assertFalse(current_user.is_active())

    # ensure logout page requires login
    def test_logout_page_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn('Please log in to access this page', response.data)


class TestUser(BaseTestCase):
    # check user can register
    def test_user_can_register(self):
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(username='testing',
                          email='test@test.com',
                          password='testing',
                          confirm='testing'),
                follow_redirects=True)
            self.assertIn('Welcome to Flask', response.data)
            self.assertTrue(current_user.name == "testing")
            self.assertTrue(current_user.is_active())
            user = User.query.filter_by(email='test@test.com').first()
            self.assertTrue(str(user) =='<name testing')

    # Ensure errors are thrown during an incorrect user registration
    def test_incorrect_user_registeration(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                    username='Michael', email='michael',
                    password='python', confirm='python'),
                                        follow_redirects=True)
            self.assertIn('Invalid email address.', response.data)
            self.assertIn('/register', request.url)

    def test_get_by_id(self):
        # Ensure id is correct for the current/logged in user
        with self.client:
            self.client.post('/login',
                             data=dict(username="admin",
                                       password='admin'),
                             follow_redirects=True)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)

    def test_check_password_hashing(self):
        # Ensure given password is correct after unhashing
        user = User.query.filter_by(email='ad@min.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

if __name__ == '__main__':
    unittest.main()
