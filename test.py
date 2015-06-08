from app import app
import unittest


class flaskTestCase(unittest.TestCase):

    # check flask correctly setup
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # check login page loads
    def test_login_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertIn('Please login', response.data)

    # check login works with correct credentials
    def test_login_works_with_correct_creds(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True)
        self.assertIn('You were just logged in', response.data)

    # check login does not work with incorrect credentials
    def test_login_does_not_work_with_incorrect_creds(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username='notadmin', password='notadmin'),
            follow_redirects=True)
        self.assertIn('Invalid credentials, Please try again.', response.data)

    # check logout works
    def test_logout_works(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn('You were just logged out', response.data)

    # ensure main page requires login
    def test_main_page_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertIn('You need to login first!', response.data)

    # ensure logout page requires login
    def test_logout_page_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn('You need to login first!', response.data)

    # ensure posts show up on main page
    def test_posts_show_up_on_main_page(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True)
        self.assertIn("I&#39;m good.", response.data)

if __name__ == '__main__':
    unittest.main()
