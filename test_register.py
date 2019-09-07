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


    def test_register_get(self):
        """Test the get response of register route"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Get Started", response.data)


    def test_register(self):
        """Test the post response of register route,
        with valid credentials"""
        response = self.client.post(
            '/register', data={
                'username': 'user2',
                'email': 'user2@gmail.com',
                'password': '1234',
                'confirm_pswd': '1234'
            }, follow_redirects=True)
        self.assertIn(b"Registered successfully. Please login", response.data)


    def test_register_email(self):
        """Test the post response of register route,
        with invalid email"""
        response = self.client.post(
            '/register', data={
                'username': 'user2',
                'email': 'user1@gmail.com',
                'password': '1234',
                'confirm_pswd': '1234'
            }, follow_redirects=True)
        self.assertIn(b"This email is aleardy exists", response.data)


    def test_register_pass(self):
        """Test the post response of register route,
        with invalid length passward"""
        response = self.client.post(
            '/register', data={
                'username': 'user2',
                'email': 'user3@gmail.com',
                'password': '1',
                'confirm_pswd': '1'
            }, follow_redirects=True)
        self.assertIn(b"Password must be between 4 and 25 charachters",
                      response.data)


    def test_register_matchpass(self):
        """Test the post response of register route,
        with unmatched passward"""
        response = self.client.post(
            '/register', data={
                'username': 'user2',
                'email': 'user3@gmail.com',
                'password': 'abcde',
                'confirm_pswd': 'abcdef'
            }, follow_redirects=True)
        self.assertIn(b"Password must match!", response.data)


    def test_register_username(self):
        """Test the post response of login route,
        with invalid username length"""
        response = self.client.post(
            '/register', data={
                'username': 'us',
                'email': 'user3@gmail.com',
                'password': '1234',
                'confirm_pswd': '1234'
            }, follow_redirects=True)
        self.assertIn(b"Username must be between 4 and 25 charachters", response.data)


if __name__ == '__main__':
    unittest.main()
