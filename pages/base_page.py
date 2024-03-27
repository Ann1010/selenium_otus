import logging
import os

import allure
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, browser, wait=3):
        self.browser = browser
        self.wait = WebDriverWait(browser, wait)
        self.actions = ActionChains(browser)
        self.logger = browser.logger
        self.class_name = type(self).__name__

    def __config_logger(self, to_file=False):
        self.logger = logging.getLogger(type(self).__name__)
        os.makedirs("logs", exist_ok=True)
        if to_file:
            self.logger.addHandler(logging.FileHandler(f"logs/{self.browser.test_name}.log"))
        self.logger.setLevel(level=self.browser.log_level)

    def open(self, url):
        self.logger.debug("%s: Opening url: %s" % (self.class_name, url))
        self.browser.get(url)

    def _text_xpath(self, text):
        return f"//*[text()='{text}']"

    def get_element(self, locator: tuple):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_elements(self, locator: tuple):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: tuple):
        self.logger.debug("%s: Clicking element: %s" % (self.class_name, str(locator)))
        element = self.get_element(locator)
        self.actions.move_to_element(element).pause(0.5).click().perform()

    def click_el(self, el):
        self.actions.move_to_element(el).pause(0.5).click().perform()

    def input_value(self, locator: tuple, text: str):
        self.logger.debug("%s: Input %s in input %s" % (self.class_name, text, locator))
        input = self.assert_element(locator)
        # input.click()
        input.clear()
        for l in text:
            input.send_keys(l)

    def assert_element(self, selector, timeout=3):
        self.logger.debug("%s: Check if element %s is present" % (self.class_name, str(selector)))
        try:
            return self.wait.until(EC.visibility_of_element_located(selector))
        except TimeoutException:
            allure.attach(
                body=self.browser.get_screenshot_as_png(),
                name="screenshot_image",
                attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Элемент {selector} не найден")

    def assert_elements(self, selector, timeout=7):
        self.logger.debug("%s: Check if elements %s is present" % (self.class_name, str(selector)))
        try:
            return self.wait.until(EC.visibility_of_all_elements_located(selector))
        except TimeoutException:
            allure.attach(
                body=self.browser.get_screenshot_as_png(),
                name="screenshot_image",
                attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Элементы {selector} не найдены")

    def search_child_element(self, parent, child):
        try:
            parent.find_element(By.XPATH, child)
        except NoSuchElementException:
            return False
        return True

    def wait_title(self, title):
        try:
            self.wait.until(EC.title_is(title))
        except TimeoutException:
            allure.attach(
                body=self.browser.get_screenshot_as_png(),
                name="screenshot_image",
                attachment_type=allure.attachment_type.PNG)
            raise AssertionError("`Ожидаемый заголовок '{}',  фактический '{}'".format(title, self.browser.title))

    def assert_text(self, selector, text):
        try:
            self.wait.until(EC.text_to_be_present_in_element(selector, text))
        except TimeoutException:
            allure.attach(
                body=self.browser.get_screenshot_as_png(),
                name="screenshot_image",
                attachment_type=allure.attachment_type.PNG)
            raise AssertionError("`Текст отличается от ожидаемого для элемента'{}'".format(selector))

    def accept_alert(self):
        alert = self.wait.until(expected_conditions.alert_is_present())
        alert.accept()

    def set_checkbox(self, checkbox, state):
        """
        Установка чекбокса
        :param checkbox: элемент
        :param state: состояние (True/False)
        :return:
        """
        if state:
            if not checkbox.get_property("checked"):
                self.click_el(checkbox)
        else:
            if checkbox.get_property("checked"):
                self.click_el(checkbox)
