from datetime import datetime
import time

from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException


class ScriptTestCase(LiveServerTestCase):
    def setUp(self):
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

    def warning_element(self):
        try:
            return self.browser.find_elements_by_css_selector(
                '#session_security_warning')[0]
        except IndexError:
            return False

    def wait_for_pages_loaded(self):
        for win in self.browser.window_handles:
            while self.warning_element() is False:
                time.sleep(0.1)

    def deadline_passed(self, now, deadline):
        return (datetime.now() - now).seconds > deadline

    def assertWarningShows(self, max_seconds):
        now = datetime.now()

        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)

            while self.warning_element() is False:
                time.sleep(0.1)

                if self.deadline_passed(now, max_seconds):
                    self.fail('Warning did not make it into DOM')

        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)

            while self.warning_element().is_displayed() is False:
                time.sleep(0.1)

                if self.deadline_passed(now, max_seconds):
                    self.fail('Warning did not make it into DOM')

    def assertWarningHides(self, max_seconds):
        now = datetime.now()

        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)

            while self.warning_element().is_displayed() is not False:
                time.sleep(0.1)

                if self.deadline_passed(now, max_seconds):
                    self.fail('Warning did not hide')

    def assertExpires(self, max_seconds):
        now = datetime.now()

        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)

            while self.warning_element() is not False:
                time.sleep(0.1)

                if self.deadline_passed(now, max_seconds):
                    self.fail('Warning did not make it out of DOM')

    def assertWarningShown(self):
        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertTrue(self.warning_element().is_displayed())

    def assertWarningHidden(self):
        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertFalse(self.warning_element().is_displayed())

    def assertWarningNotInPage(self):
        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertTrue(self.warning_element() is False)


    def test_single_window_inactivity(self):
        self.wait_for_pages_loaded()
        self.assertWarningHidden()
        self.assertWarningShows(9)
        self.assertExpires(9)

    def test_single_dont_show_warning(self):
        self.wait_for_pages_loaded()
        self.assertWarningHidden()
        time.sleep(3.5)
        self.press_space()
        self.assertWarningHidden()
        time.sleep(4)
        self.assertWarningHidden()

    def test_single_hide_warning(self):
        self.assertWarningShows(9)
        self.press_space()
        self.assertWarningHides(2)

    def test_double_window_inactivity(self):
        self.new_window()
        self.wait_for_pages_loaded()
        self.assertWarningHidden()
        self.assertWarningShows(9)
        self.assertExpires(9)

    def test_double_dont_show_warning(self):
        self.new_window()
        self.wait_for_pages_loaded()
        self.assertWarningHidden()
        time.sleep(3.5)
        self.press_space()
        self.assertWarningHidden()
        time.sleep(4)
        self.assertWarningHidden()

    def test_double_hide_warning(self):
        self.new_window()
        self.assertWarningShows(9)
        self.press_space()
        self.assertWarningHides(6)
