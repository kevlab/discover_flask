import unittest
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

if __name__ == '__main__':
    unittest.main()
