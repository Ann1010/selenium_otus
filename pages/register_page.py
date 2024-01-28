import time

from selenium.webdriver.common.by import By

from .base_page import BasePage


class RegisterPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "input-firstname")
    LASTNAME_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    NEWSLETTER_TUMBLER = (By.ID, "input-newsletter")
    AGREE_TUMBLER = (By.XPATH, "//input[@name='agree']")
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue')]")

    def register_user(self, first_name: str, lastname: str,
                    email: str, password: str):
        """Регистрация пользователя"""
        self.input_value(self.FIRST_NAME_INPUT, first_name)
        self.input_value(self.LASTNAME_INPUT, lastname)
        self.input_value(self.EMAIL_INPUT, email)
        self.input_value(self.PASSWORD_INPUT, password)
        continue_button = self.assert_element(self.CONTINUE_BUTTON)
        agree_tumbler = self.assert_element(self.AGREE_TUMBLER)
        self.browser.execute_script("arguments[0].scrollIntoView();", continue_button)
        time.sleep(1)
        self.set_checkbox(agree_tumbler, True)
        self.click(self.CONTINUE_BUTTON)
        self.wait_title('Your Account Has Been Created!', timeout=2)


