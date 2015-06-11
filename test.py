import unittest
from flask.ext.testing import TestCase
from flask.ext.login import current_user
from project import app, db
from project.models import BlogPost, User


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(BlogPost("Test post", "This is a test. Only a test."))
        db.session.add(User("admin", "ad@min.com", "admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class flaskTestCase(BaseTestCase):

    # check flask correctly setup
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # ensure main page requires login
    def test_main_page_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn('Please log in to access this page', response.data)

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

if __name__ == '__main__':
    unittest.main()
