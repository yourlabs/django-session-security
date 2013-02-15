import time
from datetime import datetime, timedelta
import unittest

from django.test.client import Client

from unittest_data_provider import data_provider


class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_anonymous(self):
        self.client.logout()
        self.client.get('/admin/')
        response = self.client.post('/session_security/ping/', {'inactiveSince': '1'})
        self.assertEqual(response.content, '["expire", -1]')

    ping_provider = lambda: (
        (1, 2, '["warn", 4]'),
        (3, 2, '["warn", 3]'),
        (0, 2, '["warn", 5]'),
        (2, 0, '["warn", 5]'),
        (5, 5, '["expire", 5]'),
        (7, 9, '["expire", 3]'),
        (8, 6, '["expire", 4]'),
        (12, 14, '["expire", -1]'),
    )

    @data_provider(ping_provider)
    def test_ping(self, server, client, expected):
        self.client.login(username='test', password='test')
        self.client.get('/admin/')

        now = datetime.now()
        session = self.client.session
        session['session_security']['last_activity'] = now - timedelta(seconds=server)
        session.save()
        response = self.client.post('/session_security/ping/', {'inactiveSince': client})
        self.assertEqual(response.content, expected)
