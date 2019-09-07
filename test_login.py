import unittest
import os
from flask import current_app
from views import app


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()


    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        """Test if the app exists """
        self.assertFalse(current_app is None)


    def test_home_page(self):
        """Test the home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


    def test_login_get(self):
        """Test the get response of login route"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter your email/password", response.data)


    def test_login(self):
        """Test the post response of login route,
        with valid credentials"""
        response = self.client.post(
            '/login', data={
                'email': 'user1@gmail.com',
                'password': '1234'
            }, follow_redirects=True)
        self.assertIn(b"You are logged in", response.data)


    def test_login_email(self):
        """Test the post response of login route,
        with invalid email"""
        response = self.client.post(
            '/login', data={
                'email': 'xxxyyuser999@gmail.com',
                'password': '1234'
            }, follow_redirects=True)
        self.assertIn(b"Email or password is incorrect", response.data)


    def test_login_pass(self):
        """Test the post response of login route,
        with invalid passward"""
        response = self.client.post(
            '/login', data={
                'email': 'user1@gmail.com',
                'password': '9999999'
            }, follow_redirects=True)
        self.assertIn(b"Email or password is incorrect", response.data)


if __name__ == '__main__':
    unittest.main()
