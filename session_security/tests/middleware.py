import time
import unittest
from datetime import datetime, timedelta

from django.test import TestCase as DjangoTestCase
from django.test.client import Client
from django.test.utils import override_settings

from session_security.utils import set_last_activity


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
        response = self.client.get('/session_security/ping/?idleFor=1')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(4)
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)


@override_settings(
    SESSION_SECURITY_EXPIRE_AFTER=3,
    SESSION_SECURITY_WARN_AFTER=2,
    SESSION_SECURITY_WARN_BEFORE=1,
    SESSION_SECURITY_CUSTOM_SESSION_KEY='user-auto-logout')
class DynamicSessionLevelTestCase(DjangoTestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='test')

    def set_custom_expire_after_value(self, value):
        s = self.client.session
        s['user-auto-logout'] = value
        s.save()

    def test_global_session_value_logout(self):
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(4)
        response = self.client.get('/admin/')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_dynamic_session_value_logout(self):
        self.set_custom_expire_after_value(2)

        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertTrue('user-auto-logout' in self.client.session)
        self.assertEqual(self.client.session.get('user-auto-logout'), 2)
        time.sleep(3)
        response = self.client.get('/admin/')
        self.assertFalse('_auth_user_id' in self.client.session)