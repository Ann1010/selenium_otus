from selenium.webdriver.common.by import By

from .base_page import BasePage


class ProductPage(BasePage):
    ADD_TO_WISHLIST_BUTTON = (By.XPATH, "//button[@title='Add to Wish List']")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[@id='button-cart']")
    COMPARE_PRODUCT_LIST = (By.XPATH, "//button[@title='Compare this Product']")
    QUANTITY_INPUT = (By.XPATH, "//input[@id='input-quantity']")
    NAV_TABS = (By.XPATH, "//*[@class='nav nav-tabs']/li/a")
    ALERT_LOGIN_ERROR = (By.XPATH, "//div[@class='alert alert-danger alert-dismissible']")
