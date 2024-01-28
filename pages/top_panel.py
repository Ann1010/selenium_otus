from selenium.webdriver.common.by import By

from .base_page import BasePage


class TopPanel(BasePage):
    CURRENCY_SELECT = (By.XPATH, "//form[@id='form-currency']//span")
    CURRENCY_ITEMS = (By.XPATH, "//form[@id='form-currency']//li/a")
    USER_BUTTON = (By.XPATH, "//i[@class='fa-solid fa-user']")
    MY_ACCOUNT_ITEM = (By.XPATH, "//a[@class='dropdown-item'][contains(text(), 'My Account')]")
    REGISTER_ITEM = (By.XPATH, "//a[@class='dropdown-item'][contains(text(), 'Register')]")
    CURRENCY_ICON = (By.XPATH, "//*[@id='form-currency']//a")

    def change_currency(self, currency: str):
        self.click(self.CURRENCY_SELECT)
        currency = self.assert_element((By.XPATH, f"//form[@id='form-currency']//li/a[contains(text(), '{currency}')]"))
        self.click_el(currency)
        # currency_list = self.assert_elements(self.CURRENCY_ITEMS)
        # for el in currency_list:
        #     if el.text == currency:
        #         el.click()
        #         break

    def open_register_form(self):
        """Открытие формы """
        self.click(self.USER_BUTTON)
        self.click(self.REGISTER_ITEM)
        self.wait_title('Register Account', timeout=2)


