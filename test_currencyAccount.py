import unittest
import os
from flask import current_app
from views import app


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        app.login_manager.init_app(app)
        app.config['LOGIN_DISABLED'] = False
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()


    def tearDown(self):
        self.app_context.pop()


    # def test_app_exists(self):
    #     """Test if the app exists """
    #     self.assertFalse(current_app is None)
    #
    #
    # def test_home_page(self):
    #     """Test the home page"""
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)


    def test_account_get(self):
        """Test the get response of register route"""
        response = self.client.get('/currency-account/4')
        print(response.data)
        self.assertIn(b"Create currency account", response.data)

    #
    # def test_account_bit(self):
    #     """Test the post response of register route,
    #     with valid credentials"""
    #     response = self.client.post(
    #         '/currency-account/4', data={
    #             'bitcoin_id': 1000,
    #             'bitcoin_balance': 10000,
    #             'ethereum_id': 9999,
    #             'ethereum_balance': 1000,
    #             'max_amount': 3000.0
    #         }, follow_redirects=True)
    #     print(response.data)
    #     self.assertIn(b"This bitcoin id is aleardy exists", response.data)
    #
    #
    # def test_account_eth(self):
    #     """Test the post response of register route,
    #     with valid credentials"""
    #     response = self.client.post(
    #         '/currency-account/4', data={
    #             'bitcoin_id': 9999,
    #             'bitcoin_balance': 10000,
    #             'ethereum_id': 1000,
    #             'ethereum_balance': 1000,
    #             'max_amount': 3000
    #         }, follow_redirects=True)
    #     print(response.data)
    #     self.assertIn(b"This ethereum id is aleardy exists", response.data)


if __name__ == '__main__':
    unittest.main()
