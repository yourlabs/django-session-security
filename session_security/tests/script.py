import time

from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException


class ScriptTestCase(LiveServerTestCase):
    def setUp(self):
        self.browsers = []

    def tearDown(self):
        for browser in self.browsers:
            browser.quit()

    def do_admin_login(self, username, password, browser):
        browser.get('%s%s' % (self.live_server_url, '/admin/'))
        username_input = browser.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = browser.find_element_by_name("password")
        password_input.send_keys(password)
        browser.find_element_by_xpath('//input[@value="Log in"]').click()

    def press_space(self, browser):
        a = ActionChains(browser)
        a.key_down(Keys.SPACE)
        a.perform()

    def warning_element(self, browser):
        try:
            return browser.find_elements_by_css_selector(
                '#session_security_warning')[0]
        except IndexError:
            return False

    def assertWarningShown(self, browser):
        self.assertTrue(self.warning_element(browser).is_displayed())

    def assertWarningHidden(self, browser):
        self.assertFalse(self.warning_element(browser).is_displayed())

    def assertWarningNotInPage(self, browser):
        self.assertTrue(self.warning_element(browser) is False)

    def test_single_window_inactivity(self):
        browser = WebDriver()
        self.browsers.append(browser)
        self.do_admin_login('test', 'test', browser)

        time.sleep(2)
        self.assertWarningHidden(browser)

        time.sleep(3+1)  # Added one second to compensate for fadeIn
        self.assertWarningShown(browser)

        time.sleep(5+1)  # Added one second to compensate for lag
        self.assertWarningNotInPage(browser)

    def test_single_dont_show_warning(self):
        browser = WebDriver()
        self.browsers.append(browser)
        self.do_admin_login('test', 'test', browser)

        time.sleep(2)
        self.press_space(browser)

        time.sleep(3+1)  # Added one seconds to compensate for fadeIn
        self.assertWarningHidden(browser)

    def test_single_hide_warning(self):
        browser = WebDriver()
        self.browsers.append(browser)
        self.do_admin_login('test', 'test', browser)

        time.sleep(5+1)  # Added one seconds to compensate for fadeIn
        self.assertWarningShown(browser)

        self.press_space(browser)
        self.assertWarningHidden(browser)

    def test_double_window_inactivity(self):
        # Disabled for now, see
        # http://stackoverflow.com/questions/14900106/how-to-prevent-django-from-overriding-sessionid-cookie
        #
        # This test would be nice to have, but is not **required** since the
        # new design which delegates all calculation of time left and next
        # action to the server (PingView)
        return

        browser0 = WebDriver()
        self.browsers.append(browser0)
        self.do_admin_login('test', 'test', browser0)
        cookie = browser0.get_cookie('sessionid')
        cookies = {'name': 'sessionid', 'value': cookie['value']}

        browser1 = WebDriver()
        self.browsers.append(browser1)
        browser1.add_cookie(cookies)
        print 1, browser0.get_cookie('sessionid')['value']
        print 2, browser1.get_cookie('sessionid')['value']
        browser1.get('%s%s' % (self.live_server_url, '/admin/'))
        print 3, browser0.get_cookie('sessionid')['value']
        print 4, browser1.get_cookie('sessionid')['value']

        self.assertEquals(browser0.get_cookie('sessionid'), browser1.get_cookie('sessionid'))

        time.sleep(2)  # give time to authenticate
        self.assertWarningHidden(browser0)
        self.assertWarningHidden(browser1)

        time.sleep(5+1)  # Added one second to compensate for fadeIn
        self.assertWarningShown(browser0)
        self.assertWarningShown(browser1)

        time.sleep(5+1)  # Added one second to compensate for lag
        self.assertWarningNotInPage(browser0)
        self.assertWarningNotInPage(browser1)
