from selenium.webdriver.common.by import By
import allure

from .base_page import BasePage


class AdministrationPage(BasePage):
    USERNAME_INPUT = (By.ID, 'input-username')
    PASSWORD_INPUT = (By.ID, 'input-password')
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    TEXT_LOGIN = (By.XPATH, "//div[@class='card-header']")
    PAGE_HEADER = (By.XPATH, "//div[@class='page-header']//h1")
    LOGOUT_BUTTON = (By.XPATH, "//*[@id='nav-logout']//span")

    def login(self, login, password):
        with allure.step("Авторизация в админке"):
            self.input_value(AdministrationPage.USERNAME_INPUT, login)
            self.input_value(AdministrationPage.PASSWORD_INPUT, password)
            self.click(AdministrationPage.SUBMIT_BUTTON)
            self.wait_title('Dashboard')
