from selenium.webdriver.common.by import By

from .base_page import BasePage


class MainPage(BasePage):
    FEATURED_PRODUCT_NAME = By.CSS_SELECTOR, "#content > div.row .product-thumb h4 a"
    SEARCH_INPUT = (By.XPATH, "//input[@name='search']")
    TABS = (By.XPATH, "//li[@class='nav-item']")
    PRODUCTS_THUMBS = (By.XPATH, "//div[@class='product-thumb']")
    BASKET_BUTTON = (By.XPATH, "//div[@id='header-cart']//button")
    BASKET_EMPTY_TEXT = (By.XPATH, "//div[@id='header-cart']//li")
    ADD_TO_CART_BUTTONS = (By.XPATH, "//button[@aria-label='Add to Cart']")
    PRODUCT_NAME_IN_CART = (By.XPATH, "//table//td[2]/a")
    PRICE_NEW = (By.XPATH, "//div[@class='description']//span[@class='price-new']")
