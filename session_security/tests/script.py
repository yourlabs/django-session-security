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

        while self.warning_element() is False:
            time.sleep(0.1)

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

    def assertWarningShown(self):
        self.assertTrue(self.warning_element().is_displayed())

    def assertWarningHidden(self):
        self.assertFalse(self.warning_element().is_displayed())

    def assertWarningNotInPage(self):
        self.assertTrue(self.warning_element() is False)

    def test_single_window_inactivity(self):
        self.assertWarningHidden()

        time.sleep(5+1)  # Added one second to compensate for fadeIn
        self.assertWarningShown()

        time.sleep(5+1)  # Added one second to compensate for lag
        self.assertWarningNotInPage()

    def test_single_dont_show_warning(self):
        self.press_space()

        time.sleep(3+1)  # Added one seconds to compensate for fadeIn
        self.assertWarningHidden()

    def test_single_hide_warning(self):
        time.sleep(5+1)  # Added one seconds to compensate for fadeIn
        self.assertWarningShown()

        self.press_space()
        self.assertWarningHidden()

    def test_double_window_inactivity(self):
        self.browser.execute_script('window.open("/admin/", "other")')

        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertWarningHidden()

        time.sleep(5+1)  # Added one second to compensate for fadeIn
        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertWarningShown()

        time.sleep(5+1)  # Added one second to compensate for lag
        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertWarningNotInPage()

    def test_double_window_hide_warning(self):
        self.browser.execute_script('window.open("/admin/", "other")')
        self.browser.switch_to_window(self.browser.window_handles[1])
        while self.warning_element() is False:
            time.sleep(0.1)
        self.browser.switch_to_window(self.browser.window_handles[0])

        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertWarningHidden()

        time.sleep(5+1)  # Added one seconds to compensate for fadeIn
        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertWarningShown()

        time.sleep(3)
        self.press_space()
        time.sleep(4)

        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertWarningHidden()

    def test_double_window_dont_show_warning(self):
        self.browser.execute_script('window.open("/admin/", "other")')

        self.press_space()
        time.sleep(3+1)

        for win in self.browser.window_handles:
            self.browser.switch_to_window(win)
            self.assertWarningHidden()
