import time
import unittest
from datetime import datetime, timedelta

from django.test import TestCase as DjangoTestCase
from django.test.client import Client

from session_security.utils import set_last_activity
from session_security import settings


class MiddlewareTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_auto_logout(self):
        self.client.login(username='test', password='test')
        self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(12)
        self.client.get('/admin/')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_last_activity_in_future(self):
        self.client.login(username='test', password='test')
        now = datetime.now()
        future = now + timedelta(0, 30)
        set_last_activity(self.client.session, future)
        self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_non_javascript_browse_no_logout(self):
        self.client.login(username='test', password='test')
        self.client.get('/admin/')
        time.sleep(8)
        self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(4)
        self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_javascript_activity_no_logout(self):
        self.client.login(username='test', password='test')
        self.client.get('/admin/')
        time.sleep(8)
        self.client.get('/session_security/ping/?idleFor=1')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(4)
        self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)


class DynamicSessionLevelTestCase(DjangoTestCase):
    def monkey_patch(self, saved_settings=None):
        values = {'EXPIRE_AFTER': 3,
                  'WARN_BEFORE': 2,
                  'WARN_AFTER': 1,
                  'EXPIRE_AFTER_CUSTOM_SESSION_KEY': 'user-session-key'}
        old_settings = {}
        for k, v in values.items():
            old_settings[k] = getattr(settings, k, None)
            setattr(
                settings, k,
                v if saved_settings is None else saved_settings.get(k))
        return old_settings

    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='test')
        self.saved_settings = self.monkey_patch()

    def tearDown(self):
        self.monkey_patch(saved_settings=self.saved_settings)

    def set_custom_expire_after_value(self, value):
        s = self.client.session
        s['user-auto-logout'] = value
        s.save()

    def test_global_session_value_logout(self):
        self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(4)
        self.client.get('/admin/')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_dynamic_session_value_logout(self):
        self.set_custom_expire_after_value(2)

        self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertTrue('user-auto-logout' in self.client.session)
        self.assertEqual(self.client.session.get('user-auto-logout'), 2)
        time.sleep(3)
        self.client.get('/admin/')
        self.assertFalse('_auth_user_id' in self.client.session)