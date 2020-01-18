import os
import time
import atexit

from django.contrib.auth.models import User

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver;
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver import Remote
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase

from selenium.common.exceptions import NoSuchElementException

from session_security.settings import WARN_AFTER, EXPIRE_AFTER


WAIT_TIME = 5 if not os.environ.get('CI', False) else 30


class SettingsMixin(object):
    def setUp(self):
        # Give some time for selenium lag
        self.min_warn_after = WARN_AFTER
        self.max_warn_after = EXPIRE_AFTER * 0.9
        self.min_expire_after = EXPIRE_AFTER
        self.max_expire_after = EXPIRE_AFTER * 1.5
        super(SettingsMixin, self).setUp()


class BaseLiveServerTestCase(SettingsMixin, StaticLiveServerTestCase,
                             LiveServerTestCase):

    fixtures = ['session_security_test_user']

    def setUp(self):
        SettingsMixin.setUp(self)
        from selenium.webdriver.firefox.options import Options as FirefoxOptions

        options = FirefoxOptions()
        options.add_argument("--headless")
        super(LiveServerTestCase, self).setUp()
        self.sel= webdriver.Firefox(options=options)
        self.sel.get('%s%s' % (self.live_server_url, '/admin/'))
        self.sel.find_element_by_name('username').send_keys('test')
        self.sel.find_element_by_name('password').send_keys('test')
        self.sel.find_element_by_xpath('//input[@value="Log in"]').click()
        self.sel.execute_script('window.open("/admin/", "other")')

    def press_space(self):
        body = self.sel.find_element_by_tag_name("body")
        body.send_keys(Keys.SPACE)
    def tearDown(self):
        self.sel.quit()
    @classmethod
    def tearDownClass(cls):
        super(BaseLiveServerTestCase, cls).tearDownClass()