# from views import app
# import unittest

import unittest
from flask import current_app
from views import app


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(
            '/login', data={
                'username': 'user1',
                'password': '1238'
            }, follow_redirects=True)
        print(response.data)
        self.assertIn(b"You are logged in", response.data)


# class FlaskTestCase(unittest.TestCase):
#
#     def test_index(self):
#         tester = app.test_client(self)
#         response = tester.get('/', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#
#     def test_login(self):
#         tester = app.test_client(self)
#         response = tester.get('/login', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#
#
#     def test_mainPage(self):
#         tester = app.test_client(self)
#         response = tester.get('/user', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#
#     def test_mainPage(self):
#         tester = app.test_client(self)
#         response = tester.get('/user', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#
#
#     def test_currencyAccount(self):
#         tester = app.test_client(self)
#         response = tester.get('/currency-account/1', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#
#         response = tester.get('/currency-account/999', content_type='html/text')
#         self.assertNotEqual(response.status_code, 200)
#
#
#     def test_EdityAccount(self):
#         tester = app.test_client(self)
#         response = tester.get('/edit-account/1', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#
#         response = tester.get('/edit-account/999', content_type='html/text')
#         self.assertNotEqual(response.status_code, 200)
#
#
#     def test_transfare(self):
#         tester = app.test_client(self)
#         response = tester.get('/transaction/1', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#
#         response = tester.get('/transaction/999', content_type='html/text')
#         self.assertNotEqual(response.status_code, 200)
#
#     def test_history(self):
#         tester = app.test_client(self)
#         response = tester.get('/transaction-history/1', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#
#         response = tester.get('/transaction-history/999', content_type='html/text')
#         self.assertNotEqual(response.status_code, 200)

    # def test_purchase_10VS5(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/purchase', data=dict(name="10 VS5"),
    #                           follow_redirects=True)
    #     print(response)
    #     self.assertIn(b"$17.98", response.data)
    #     self.assertIn(b"2 x 5 $8.99", response.data)
    #
    #
    # def test_purchase_14MB11(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/purchase', data=dict(name="14 MB11"),
    #                           follow_redirects=True)
    #     print(response)
    #     self.assertIn(b"$54.80", response.data)
    #     self.assertIn(b"1 x 8 $24.95 3 x 2 $9.95", response.data)
    #
    #
    # def test_purchase_13CF(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/purchase', data=dict(name="13 CF"),
    #                           follow_redirects=True)
    #     print(response)
    #     self.assertIn(b"$25.85", response.data)
    #     self.assertIn(b"2 x 5 $9.95 1 x 3 $5.95", response.data)




if __name__ == '__main__':
    unittest.main()
