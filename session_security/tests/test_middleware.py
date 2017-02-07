import time
import unittest

from django.test.client import Client
from django import test
from session_security.utils import set_last_activity, get_last_activity
from datetime import datetime, timedelta

from .test_base import SettingsMixin


class MiddlewareTestCase(SettingsMixin, test.TestCase):
    fixtures = ['session_security_test_user']

    def setUp(self):
        super(MiddlewareTestCase, self).setUp()
        self.client = Client()

    def test_auto_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(self.max_expire_after)
        response = self.client.get('/admin/')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_last_activity_in_future(self):
        self.client.login(username='test', password='test')
        now = datetime.now()
        future = now + timedelta(0, self.max_expire_after * 2)
        set_last_activity(self.client.session, future)
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_non_javascript_browse_no_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/admin/')
        time.sleep(self.max_warn_after)
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(self.min_warn_after)
        response = self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_javascript_activity_no_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/admin/')
        time.sleep(self.max_warn_after)
        self.client.get('/session_security/ping/?idleFor=1')
        self.assertTrue('_auth_user_id' in self.client.session)
        time.sleep(self.min_warn_after)
        self.client.get('/admin/')
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_url_names(self):
        self.client.login(username='test', password='test')
        # Confirm activity is updating
        response = self.client.get('/admin/')
        activity1 = get_last_activity(self.client.session)
        time.sleep(min(2, self.min_warn_after))
        response = self.client.get('/admin/')
        activity2 = get_last_activity(self.client.session)
        self.assertTrue(activity2 > activity1)
        # Confirm activity on ignored URL is NOT updated
        time.sleep(min(2, self.min_warn_after))
        response = self.client.get('/ignore/')
        activity3 = get_last_activity(self.client.session)
        self.assertEqual(activity2, activity3)
