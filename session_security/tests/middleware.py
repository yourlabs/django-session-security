import time
import unittest

from django.test.client import Client
from session_security.utils import set_last_activity
from datetime import datetime, timedelta

from .base import get_or_create_test_admin


class MiddlewareTestCase(unittest.TestCase):
    def setUp(self):
        get_or_create_test_admin()
        self.client = Client()

    def test_auto_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(12)
        response = self.client.get('/admin/')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_last_activity_in_future(self):
        self.client.login(username='test', password='test')
        now = datetime.now()
        future = now + timedelta(0, 30)
        set_last_activity(self.client.session, future)
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)

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
        self.client.get('/session_security/ping/?idleFor=1')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(4)
        self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
