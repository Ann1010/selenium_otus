from selenium.webdriver.common.by import By

from .base_page import BasePage


class NavigationPanel(BasePage):
    MENU_CATALOG = By.XPATH, "//li[@id='menu-catalog']"

    def expand_menu(self, menu: str):
        self.click((By.XPATH, f"//li[@id='menu-{menu}']"))

    def go_to_tab(self, menu, tab):
        self.expand_menu(menu)
        self.click((By.XPATH, f"//a[contains(@href, '{menu}/{tab}')]"))
