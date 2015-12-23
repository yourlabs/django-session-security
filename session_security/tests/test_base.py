import os
import time
import atexit

from django.contrib.auth.models import User

from sbo_selenium import SeleniumTestCase

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver import Remote
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

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
                             SeleniumTestCase):

    fixtures = ['session_security_test_user']

    def setUp(self):
        super(BaseLiveServerTestCase, self).setUp()
        self.get('/admin/')
        self.sel.find_element_by_name('username').send_keys('test')
        self.sel.find_element_by_name('password').send_keys('test')
        self.sel.find_element_by_xpath('//input[@value="Log in"]').click()
        self.sel.execute_script('window.open("/admin/", "other")')

    def press_space(self):
        a = ActionChains(self.sel)
        a.key_down(Keys.SPACE)
        a.perform()
