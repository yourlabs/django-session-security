from __future__ import unicode_literals

import six

import time
from datetime import datetime, timedelta
import unittest

from django.test.utils import override_settings
from django.test.client import Client
from django import test

from unittest_data_provider import data_provider

from session_security.utils import set_last_activity
from session_security import settings


class ViewsTestCase(test.TestCase):
    fixtures = ['session_security_test_user']

    def setUp(self):
        self.client = Client()

    def test_anonymous(self):
        self.client.logout()
        self.client.get('/admin/')
        response = self.client.get('/session_security/ping/?idleFor=1')
        self.assertEqual(response.content, six.b('"logout"'))

    def ping_provider(x=None):
        return (
            (1, 4, '1'),
            (3, 2, '2'),
            (5, 5, '5'),
            (12, 14, '"logout"', False),
        )

    @data_provider(ping_provider)
    def test_ping(self, server, client, expected, authenticated=True):
        old_warn, old_expire = settings.WARN_AFTER, settings.EXPIRE_AFTER
        settings.WARN_AFTER, settings.EXPIRE_AFTER = 5, 10

        self.client.login(username='test', password='test')
        self.client.get('/admin/')

        now = datetime.now()
        session = self.client.session
        set_last_activity(session, now - timedelta(seconds=server))
        session.save()
        response = self.client.get('/session_security/ping/?idleFor=%s' %
                                   client)

        self.assertEqual(response.content, six.b(expected))
        self.assertEqual(authenticated, '_auth_user_id' in self.client.session)

        settings.WARN_AFTER, settings.EXPIRE_AFTER = old_warn, old_expire
