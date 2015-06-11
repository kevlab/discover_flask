import unittest
from flask.ext.login import current_user
from base import BaseTestCase


class flaskTestCase(BaseTestCase):

    # check flask correctly setup
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # ensure main page requires login
    def test_main_page_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn('Please log in to access this page', response.data)

    # Ensure that welcome page loads
    def test_welcome_route_works_as_expected(self):
        response = self.client.get('/welcome', follow_redirects=True)
        self.assertIn(b'Welcome to Flask', response.data)

    # ensure posts show up on main page
    def test_posts_show_up_on_main_page(self):
        response = self.client.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True)
        self.assertIn("This is a test.", response.data)


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

if __name__ == '__main__':
    unittest.main()
