import unittest
import os
from flask import current_app
from views import app


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        app.login_manager.init_app(app)
        app.config['LOGIN_DISABLED'] = True
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


    def test_transfare_get(self):
        """Test the get response of register route"""
        response = self.client.get('/transaction/1')
        print(response.data)
        self.assertIn(b"Transfare Money", response.data)


    def test_currency_type(self):
        """Test the post response of transaction route,
        with invalid currency type"""
        response = self.client.post(
            '/transaction/1', data={
                'currency_amount': 1000,
                'currency_Type': 'USD',
                'target_user': 2,
            }, follow_redirects=True)
        print(response.data)
        self.assertIn(b"The currency type should be bitcoin or ethereum", response.data)


    def test_user_account(self):
        """Test the post response of transaction route,
        with invalid target account"""
        response = self.client.post(
            '/transaction/1', data={
                'currency_amount': 1000,
                'currency_Type': 'bitcoin',
                'target_user': 3,
            }, follow_redirects=True)
        print(response.data)
        self.assertIn(b"This user has no currency account!", response.data)


    def test_user_exists(self):
        """Test the post response of transaction route,
        with invalid target user"""
        response = self.client.post(
            '/transaction/1', data={
                'currency_amount': 1000,
                'currency_Type': 'bitcoin',
                'target_user': 999,
            }, follow_redirects=True)
        print(response.data)
        self.assertIn(b"This user is not exists, Please check the ID", response.data)


if __name__ == '__main__':
    unittest.main()
