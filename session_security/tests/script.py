from datetime import datetime
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from .base import BaseLiveServerTestCase

class ScriptTestCase(BaseLiveServerTestCase):
    def warning_element(self):
        try:
            return self.browser.find_elements_by_css_selector(
                '#session_security_warning')[0]
        except IndexError:
            return False

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
