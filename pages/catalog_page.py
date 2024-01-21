from selenium.webdriver.common.by import By

from .base_page import BasePage


class CatalogPage(BasePage):
    LEFT_MENU = (By.ID, "column-left")
    COMPARE_BUTTON = (By.ID, "compare-total")
    INPUT_SORT = (By.ID, "input-sort")
    INPUT_LIMIT = (By.ID, "input-limit")
    LIMITS = (By.XPATH, "//*[@id='input-limit']/option")
    PRODUCT_PRICE = (By.XPATH, "//div[@id='product-info']//span[@class='price-tax']")