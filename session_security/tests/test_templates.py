from django.contrib.auth.models import User
from django.test import TestCase, override_settings


class TemplateTests(TestCase):

    def setUp(self):
        self.user = User(
            username='test'
        )
        self.user.save()

    def test_default(self):
        """The default template should not include an entry for `returnToUrl`"""
        self.client.force_login(self.user)
        resp = self.client.get(
            '/template/'
        )

        self.assertNotIn(
            'returnToUrl',
            resp.content
        )

    def test_setting(self):
        """The default template should include an entry for `returnToUrl`"""
        self.client.force_login(self.user)
        with self.settings(SESSION_SECURITY_REDIRECT_TO_LOGOUT=True):
            resp = self.client.get(
                '/template/'
            )

        self.assertIn(
            'returnToUrl',
            resp.content
        )
