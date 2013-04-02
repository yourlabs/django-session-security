import time
import unittest

from django.test.client import Client


class MiddlewareTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_auto_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(12)
        response = self.client.get('/admin/')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_non_javascript_browse_no_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/admin/')
        time.sleep(8)
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(4)
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_javascript_activity_no_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/admin/')
        time.sleep(8)
        response = self.client.get('/session_security/ping/?idleFor=1')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(4)
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
