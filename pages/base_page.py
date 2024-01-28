from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def _text_xpath(self, text):
        return f"//*[text()='{text}']"

    def get_element(self, locator: tuple, timeout=5):
        return WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))

    def get_elements(self, locator: tuple, timeout=3):
        return WebDriverWait(self.browser, timeout).until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: tuple):
        element = self.get_element(locator)
        ActionChains(self.browser).move_to_element(element).pause(0.5).click().perform()

    def click_el(self, el):
        ActionChains(self.browser).move_to_element(el).pause(0.5).click().perform()

    def input_value(self, locator: tuple, text: str):
        input = self.assert_element(locator)
        # input.click()
        input.clear()
        for l in text:
            input.send_keys(l)

    def assert_element(self, selector, timeout=3):
        try:
            return WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(selector))
        except TimeoutException:
            self.browser.save_screenshot("{}.png".format(self.browser.session_id))
            raise AssertionError(f"Элемент {selector} не найден")

    def assert_elements(self, selector, timeout=7):
        try:
            return WebDriverWait(self.browser, timeout).until(EC.visibility_of_all_elements_located(selector))
        except TimeoutException:
            self.browser.save_screenshot("{}.png".format(self.browser.session_id))
            raise AssertionError(f"Элементы {selector} не найдены")

    def search_child_element(self, parent, child):
        try:
            parent.find_element(By.XPATH, child)
        except NoSuchElementException:
            return False
        return True

    def wait_title(self, title, timeout=3):
        try:
            WebDriverWait(self.browser, timeout).until(EC.title_is(title))
        except TimeoutException:
            raise AssertionError("`Ожидаемый заголовок '{}',  фактический '{}'".format(title, self.browser.title))

    def assert_text(self, selector, text, timeout=3):
        try:
            WebDriverWait(self.browser, timeout).until(EC.text_to_be_present_in_element(selector, text))
        except TimeoutException:
            raise AssertionError("`Текст отличается от ожидаемого для элемента'{}'".format(selector))

    def accept_alert(self):
        alert = WebDriverWait(self.browser, timeout=3).until(expected_conditions.alert_is_present())
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
