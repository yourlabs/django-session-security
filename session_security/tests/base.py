import time

from django.contrib.auth.models import User

try:
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase as \
        LiveServerTestCase
except ImportError:
    from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException


def get_or_create_test_admin():
    u, c = User.objects.get_or_create(username='test')

    if c:
        u.is_staff = True
        u.set_password('test')
        u.save()

    return u


class BaseLiveServerTestCase(LiveServerTestCase):
    def setUp(self):
        get_or_create_test_admin()
        self.browser = WebDriver()
        self.do_admin_login('test', 'test')

    def tearDown(self):
        self.browser.quit()

    def do_admin_login(self, username, password):
        self.browser.get('%s%s' % (self.live_server_url, '/admin/'))
        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys(password)
        self.browser.find_element_by_xpath('//input[@value="Log in"]').click()

    def new_window(self, name='other'):
        self.browser.execute_script('window.open("/admin/", "'+ name +'")')
        self.browser.switch_to_window(self.browser.window_handles[1])
        while self.warning_element() is False:
            time.sleep(0.1)
        self.browser.switch_to_window(self.browser.window_handles[0])

    def press_space(self):
        a = ActionChains(self.browser)
        a.key_down(Keys.SPACE)
        a.perform()

    def wait_for_pages_loaded(self):
        for win in self.browser.window_handles:
            while self.warning_element() is False:
                time.sleep(0.1)
