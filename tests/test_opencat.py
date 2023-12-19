import random
import time

import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# MainPageLocators
SEARCH_INPUT = (By.XPATH, "//input[@name='search']")
TABS = (By.XPATH, "//li[@class='nav-item']")
PRODUCTS_THUMBS = (By.XPATH, "//div[@class='product-thumb']")
BASKET_BUTTON = (By.XPATH, "//div[@id='header-cart']//button")
BASKET_EMPTY_TEXT = (By.XPATH, "//div[@id='header-cart']//li")
ADD_TO_CART_BUTTONS = (By.XPATH, "//button[@aria-label='Add to Cart']")
PRODUCT_NAME_IN_CART = (By.XPATH, "//table//td[2]/a")
CURRENCY_SELECT = (By.XPATH, "//form[@id='form-currency']//span")
CURRENCY_ITEMS = (By.XPATH, "//form[@id='form-currency']//li/a")
PRICE_NEW = (By.XPATH, "//span[@class='price-tax']")

# Catalog
LEFT_MENU = (By.ID, "column-left")
COMPARE_BUTTON = (By.ID, "compare-total")
INPUT_SORT = (By.ID, "input-sort")
INPUT_LIMIT = (By.ID, "input-limit")
LIMITS = (By.XPATH, "//*[@id='input-limit']/option")
PRODUCT_PRICE = (By.XPATH, "//div[@id='product-info']//span[@class='price-tax']")

# Product Page
ADD_TO_WISHLIST_BUTTON = (By.XPATH, "//button[@title='Add to Wish List']")
ADD_TO_CART_BUTTON = (By.XPATH, "//button[@id='button-cart']")
COMPARE_PRODUCT_LIST = (By.XPATH, "//button[@title='Compare this Product']")
QUANTITY_INPUT = (By.XPATH, "//input[@id='input-quantity']")
NAV_TABS = (By.XPATH, "//*[@class='nav nav-tabs']/li/a")
ALERT_LOGIN_ERROR = (By.XPATH, "//div[@class='alert alert-danger alert-dismissible']")

# Аdministration Page
USERNAME_INPUT = (By.ID, 'input-username')
PASSWORD_INPUT = (By.ID, 'input-password')
SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
TEXT_LOGIN = (By.XPATH, "//div[@class='card-header']")
PAGE_HEADER = (By.XPATH, "//div[@class='page-header']//h1")
LOGOUT_BUTTON = (By.XPATH, "//*[@id='nav-logout']//span")

# Register Page
FIRST_NAME_INPUT = (By.ID, "input-firstname")
LASTNAME_INPUT = (By.ID, "input-lastname")
EMAIL_INPUT = (By.ID, "input-email")
NEWSLETTER_TUMBLER = (By.ID, "input-newsletter")


def search_child_element(selector, child):
    try:
        selector.find_element(By.XPATH, child)
    except NoSuchElementException:
        return False
    return True


def assert_element(selector: object, driver: object, timeout: object = 3) -> object:
    try:
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(selector))
    except TimeoutException:
        driver.save_screenshot("{}.png".format(driver.session_id))
        raise AssertionError(f"Элемент {selector} не найден")


def assert_elements(selector, driver, timeout=7):
    try:
        return WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located(selector))
    except TimeoutException:
        driver.save_screenshot("{}.png".format(driver.session_id))
        raise AssertionError(f"Элементы {selector} не найдены")


def wait_title(title: str, driver: object, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(EC.title_is(title))
    except TimeoutException:
        raise AssertionError("`Ожидаемый заголовок '{}',  фактический '{}'".format(title, driver.title))


def assert_text(selector, text, driver, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element(selector, text))
    except TimeoutException:
        raise AssertionError("`Текст отличается от ожидаемого для элемента'{}'".format(selector))


def change_currency(currency: str, browser):
    assert_element(CURRENCY_SELECT, browser).click()
    currency_list = assert_elements(CURRENCY_ITEMS, browser)
    for el in currency_list:
        if el.text == currency:
            el.click()
            break


@pytest.mark.main_page
def test_check_main_page(browser, base_url):
    """
    # 1 - Проверка отображения поля ввода Поиск
    # 2 - Проверка отображения табов и их названий
    # 3 - Проверка отображения блоков с продуктами, наличие их изображений и описаний
    # 4 - Проверка отображения кнопки Корзина
    # 5 - Клик по пустой корзине и проверка отображения текста Your shopping cart is empty!
    """
    browser.get(base_url)
    # 1
    assert_element(SEARCH_INPUT, browser)
    # 2
    tabs = assert_elements(TABS, browser)
    tabs_name = ['Desktops', 'Laptops & Notebooks', 'Components', 'Tablets', 'Software',
                 'Phones & PDAs', 'Cameras', 'MP3 Players']
    for tab in tabs:
        assert tab.text in tabs_name, \
            "Список разделов отличается от ожидаемого"
    # 3
    products = assert_elements(PRODUCTS_THUMBS, browser)
    for product in products:
        assert search_child_element(product, ".//div[@class='image']")
        assert search_child_element(product, ".//div[@class='description']")
    # 4
    basket = assert_element(BASKET_BUTTON, browser)
    # 5
    basket.click()
    basket_empty_text = assert_element(BASKET_EMPTY_TEXT, browser)
    assert basket_empty_text.text == 'Your shopping cart is empty!'
    assert_element((By.XPATH, "//*[@title='Your Store']"), browser).click()

    # Проверка смены валюты
    current_price_new = assert_elements(PRICE_NEW, browser)
    current_price_text = [price.text for price in current_price_new]
    change_currency('€ Euro', browser)
    new_price = assert_elements(PRICE_NEW, browser)
    new_price_text = [price.text for price in new_price]
    for i in range(len(new_price_text)):
        assert current_price_text[i] != new_price_text[i], \
            'При смене валюты не изменилась цена продуктов'

    # Проверка добавления товара в корзину
    products = assert_elements((By.XPATH, "//div[@class='content']"), browser)
    choose_product = random.randint(0, len(products)-1)
    product_name = products[choose_product].find_element(By.XPATH, ".//h4/a")
    add_button_icon = products[choose_product].find_element(By.XPATH, ".//i[@class='fa-solid fa-shopping-cart']")
    add_button_icon.click()
    time.sleep(1)
    if browser.title != 'Your Store':
        # Продукты с вариативными характеристиками не сразу добавляются в корзину,
        # происходит переход на страницу продукта.
        # Нужно ли протестировать этот вариант?
        pass
    else:
        assert_element((By.XPATH, "//button[@class='btn-close']"), browser).click()
        assert_element(BASKET_BUTTON, browser).click()
        product_in_cart = assert_element(PRODUCT_NAME_IN_CART, browser).text
        assert product_in_cart == product_name.text, \
            f"Название продукта в корзине {product_in_cart} отличается от ожидаемого {product_name.text}"


@pytest.mark.catalog
@pytest.mark.parametrize('tab', ['desktops', 'laptop-notebook'])
def test_check_catalog_page(browser, base_url, tab):
    """
    # 1 - Проверка отображения бокового меню
    # 2 - Проверка отображения кнопки сравнения продуктов
    # 3 - Проверка отображения поля Сортировки
    # 4 - Проверка отображения поля выбора количества продуктов на странице
    # 5 - Проверка отображений вариантов количества продуктов на странице
    """
    browser.get(f"{base_url}/en-gb/catalog/{tab}")
    # 1
    assert_element(LEFT_MENU, browser)
    # 2
    assert_element(COMPARE_BUTTON, browser)
    # 3
    assert_element(INPUT_SORT, browser)
    # 4
    limit_input = assert_element(INPUT_LIMIT, browser)
    # 5
    limit_input.click()
    limits = assert_elements(LIMITS, browser)
    limits_list = ['10', '25', '50', '75', '100']
    for limit in limits:
        assert limit.text in limits_list

    # Проверка смены валюты
    current_price_new = assert_elements(PRICE_NEW, browser)
    current_price_text = [price.text for price in current_price_new]
    change_currency(currency='€ Euro', browser=browser)
    # При смене валюты происходит переход на главную страницу, поэтому снова возвращаемся в каталог
    browser.get(f"{base_url}/en-gb/catalog/{tab}")
    new_price = assert_elements(PRICE_NEW, browser)
    new_price_text = [price.text for price in new_price]
    for i in range(len(current_price_text)):
        assert current_price_text[i] != new_price_text[i], \
            'При смене валюты не изменилась цена продуктов'


@pytest.mark.product
@pytest.mark.parametrize('product', ['macbook', 'iphone'])
def test_check_product_page(browser, base_url, product):
    """
    # 1 - Проверка отображения кнопки Добавить в избранное
    # 2 - Проверка отображения кнопки Добавить в корзину
    # 3 - Проверка отображения кнопки Сравнить продукт для сравнения
    # 4 - Проверка отображения поля ввода количества продуктов
    # 5 - Проверка отображения разделов
    # 6 - Проверка названий разделов
    """
    browser.get(f"{base_url}/en-gb/product/{product}")
    # 1
    assert_element(ADD_TO_WISHLIST_BUTTON, browser)
    # 2
    assert_element(ADD_TO_CART_BUTTON, browser)
    # 3
    assert_element(COMPARE_PRODUCT_LIST, browser)
    # 4
    assert_element(QUANTITY_INPUT, browser)
    # 5
    nav_tabs = assert_elements(NAV_TABS, browser)
    # 6
    tabs = ['Description', 'Specification', 'Reviews']
    for tab in nav_tabs:
        assert tab.text.split(" ")[0] in tabs, \
            f'Вкладка {tab.text.split(" ")[0]} отсутствует в списке ожидаемых'


@pytest.mark.administration
def test_check_login_page(browser, base_url):
    """
    # 1 - Проверка отображения поля ввода логина
    # 2 - Проверка отображения поля ввода пароля
    # 3 - Проверка отображения кнопки Login
    # 4 - Проверка отображения уточняющего текста
    # 5 - Проверка отображения всплывающей ошибки при неправильных кредах
    """
    login = 'user'
    password = 'bitnami'
    browser.get(f"{base_url}/administration/")
    # 1
    assert_element(USERNAME_INPUT, browser)
    # 2
    assert_element(PASSWORD_INPUT, browser)
    # 3
    submit_button = assert_element(SUBMIT_BUTTON, browser)
    # 4
    assert_text(TEXT_LOGIN, 'Please enter your login details.', browser)
    # 5
    submit_button.click()
    assert_element(ALERT_LOGIN_ERROR, browser)
    # Проверка логина/разлогина
    assert_element(USERNAME_INPUT, browser).send_keys(login)
    assert_element(PASSWORD_INPUT, browser).send_keys(password)
    submit_button.click()
    wait_title('Dashboard', browser)
    assert_text(PAGE_HEADER, 'Dashboard', browser)
    logout = assert_element(LOGOUT_BUTTON, browser)
    logout.click()
    wait_title('Administration', browser)
    assert_element(USERNAME_INPUT, browser)


@pytest.mark.register
def test_check_register_page(browser, base_url):
    """
    # 1 - Проверка отображения поля ввода First Name
    # 2 - Проверка отображения поля ввода Last Name
    # 3 - Проверка отображения поля ввода E-mail
    # 4 - Проверка отображения поля ввода Пароль
    # 5 - Проверка отображения тумблера Subscribe
    """
    browser.get(f"{base_url}/index.php?route=account/register")
    # 1
    assert_element(FIRST_NAME_INPUT, browser)
    # 2
    assert_element(LASTNAME_INPUT, browser)
    # 3
    assert_element(EMAIL_INPUT, browser)
    # 4
    assert_element(PASSWORD_INPUT, browser)
    # 5
    assert_element(NEWSLETTER_TUMBLER, browser)
