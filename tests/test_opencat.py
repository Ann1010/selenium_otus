import random
import time

import pytest
from selenium.webdriver.common.by import By

from ..help import random_email
from ..pages.administration_page import AdministrationPage
from ..pages.administration_pages.admin_products_page import AdminProductPage
from ..pages.catalog_page import CatalogPage
from ..pages.main_page import MainPage
from ..pages.navigation_panel import NavigationPanel
from ..pages.product_page import ProductPage
from ..pages.register_page import RegisterPage
from ..pages.top_panel import TopPanel


@pytest.mark.main_page
def test_check_main_page(browser):
    """
    Проверка отображения поля ввода Поиск
    Проверка отображения табов и их названий
    Проверка отображения блоков с продуктами, наличие их изображений и описаний
    Проверка отображения кнопки Корзина
    Клик по пустой корзине и проверка отображения текста Your shopping cart is empty!
    Проверка смены валюты
    Проверка добавления товара в корзину
    """
    page = MainPage(browser)
    page.assert_element(MainPage.SEARCH_INPUT)
    tabs = page.assert_elements(MainPage.TABS)
    tabs_name = ['Desktops', 'Laptops & Notebooks', 'Components', 'Tablets', 'Software',
                 'Phones & PDAs', 'Cameras', 'MP3 Players']
    for tab in tabs:
        assert tab.text in tabs_name, \
            "Список разделов отличается от ожидаемого"
    products = page.assert_elements(MainPage.PRODUCTS_THUMBS)
    for product in products:
        assert page.search_child_element(product, ".//div[@class='image']"), \
            "У продукта не отображается изображение"
        assert page.search_child_element(product, ".//div[@class='description']"), \
            "У продукта не отображается описание"
    page.assert_element(MainPage.BASKET_BUTTON)
    page.click(MainPage.BASKET_BUTTON)
    basket_empty_text = page.assert_element(MainPage.BASKET_EMPTY_TEXT).text
    assert basket_empty_text == 'Your shopping cart is empty!', \
        "Для пустой корзины не отображается сообщение 'Your shopping cart is empty!'"
    page.click((By.XPATH, "//*[@title='Your Store']"))
    # Проверка смены валюты
    current_price_new = page.assert_elements(MainPage.PRICE_NEW)
    current_price_text = [price.text for price in current_price_new]
    TopPanel(browser).change_currency('€ Euro')
    new_price = page.assert_elements(MainPage.PRICE_NEW)
    new_price_text = [price.text for price in new_price]
    for i in range(len(new_price_text)):
        assert current_price_text[i] != new_price_text[i], \
            'При смене валюты не изменилась цена продуктов'
    # Проверка добавления товара в корзину
    products = page.assert_elements((By.XPATH, "//div[@class='content']"))
    choose_product = random.randint(0, len(products) - 1)
    product_name = products[choose_product].find_element(By.XPATH, ".//h4/a").text
    add_button_icon = products[choose_product].find_element(By.XPATH, ".//button[1]")
    page.click_el(add_button_icon)
    time.sleep(1)
    if browser.title != 'Your Store':
        pass
    else:
        page.click((By.XPATH, "//button[@class='btn-close']"))
        page.click(MainPage.BASKET_BUTTON)
        product_in_cart = page.assert_element(MainPage.PRODUCT_NAME_IN_CART).text
        assert product_in_cart == product_name, \
            f"Название продукта в корзине {product_in_cart} отличается от ожидаемого {product_name.text}"


@pytest.mark.catalog
@pytest.mark.parametrize('tab', ['desktops', 'laptop-notebook'])
def test_check_catalog_page(browser, url, tab):
    """
    Проверка отображения бокового меню
    Проверка отображения кнопки сравнения продуктов
    Проверка отображения поля Сортировки
    Проверка отображения поля выбора количества продуктов на странице
    Проверка отображений вариантов количества продуктов на странице
    """
    page = CatalogPage(browser)
    browser.get(f"{url}/en-gb/catalog/{tab}")
    page.assert_element(CatalogPage.LEFT_MENU)
    page.assert_element(CatalogPage.COMPARE_BUTTON)
    page.assert_element(CatalogPage.INPUT_SORT)

    page.click(CatalogPage.INPUT_LIMIT)
    limits = page.assert_elements(CatalogPage.LIMITS)
    limits_list = ['10', '25', '50', '75', '100']
    for limit in limits:
        assert limit.text in limits_list
    # Проверка смены валюты
    current_price_new = page.assert_elements(MainPage.PRICE_NEW)
    current_price_text = [price.text for price in current_price_new]
    TopPanel(browser).change_currency('€ Euro')
    # При смене валюты происходит переход на главную страницу, поэтому снова возвращаемся в каталог
    browser.get(f"{url}/en-gb/catalog/{tab}")
    new_price = page.assert_elements(MainPage.PRICE_NEW)
    new_price_text = [price.text for price in new_price]
    for i in range(len(current_price_text)):
        assert current_price_text[i] != new_price_text[i], \
            'При смене валюты не изменилась цена продуктов'


@pytest.mark.product
@pytest.mark.parametrize('product', ['macbook', 'iphone'])
def test_check_product_page(browser, url, product):
    """
    Проверка отображения кнопки Добавить в избранное
    Проверка отображения кнопки Добавить в корзину
    Проверка отображения кнопки Сравнить продукт для сравнения
    Проверка отображения поля ввода количества продуктов
    Проверка отображения разделов
    Проверка названий разделов
    """
    page = ProductPage(browser)
    browser.get(f"{url}/en-gb/product/{product}")
    page.assert_element(ProductPage.ADD_TO_WISHLIST_BUTTON)
    page.assert_element(ProductPage.ADD_TO_CART_BUTTON)
    page.assert_element(ProductPage.COMPARE_PRODUCT_LIST)
    page.assert_element(ProductPage.QUANTITY_INPUT)
    nav_tabs = page.assert_elements(ProductPage.NAV_TABS)
    tabs = ['Description', 'Specification', 'Reviews']
    for tab in nav_tabs:
        assert tab.text.split(" ")[0] in tabs, \
            f'Вкладка {tab.text.split(" ")[0]} отсутствует в списке ожидаемых'


@pytest.mark.administration
def test_check_login_page(browser, url):
    """
    Проверка отображения поля ввода логина
    Проверка отображения поля ввода пароля
    Проверка отображения кнопки Login
    Проверка отображения уточняющего текста
    Проверка отображения всплывающей ошибки при неправильных кредах
    """
    page = AdministrationPage(browser)
    browser.get(f"{url}/administration/")

    login = 'user'
    password = 'bitnami'
    page.assert_element(AdministrationPage.USERNAME_INPUT)
    page.assert_element(AdministrationPage.PASSWORD_INPUT)
    page.assert_element(AdministrationPage.SUBMIT_BUTTON)
    page.assert_text(AdministrationPage.TEXT_LOGIN, 'Please enter your login details.')
    page.click(AdministrationPage.SUBMIT_BUTTON)
    page.assert_element(ProductPage.ALERT_LOGIN_ERROR)
    # Проверка логина/разлогина
    page.input_value(AdministrationPage.USERNAME_INPUT, login)
    page.input_value(AdministrationPage.PASSWORD_INPUT, password)
    page.click(AdministrationPage.SUBMIT_BUTTON)
    page.wait_title('Dashboard')
    page.assert_text(AdministrationPage.PAGE_HEADER, 'Dashboard')
    page.click(AdministrationPage.LOGOUT_BUTTON)
    page.wait_title('Administration')
    page.assert_element(AdministrationPage.USERNAME_INPUT)


@pytest.mark.register
def test_check_register_page(browser, url):
    """
    Проверка отображения поля ввода First Name
    Проверка отображения поля ввода Last Name
    Проверка отображения поля ввода E-mail
    Проверка отображения поля ввода Пароль
    Проверка отображения тумблера Subscribe
    """
    page = RegisterPage(browser)
    browser.get(f"{url}/index.php?route=account/register")
    page.assert_element(RegisterPage.FIRST_NAME_INPUT)
    page.assert_element(RegisterPage.LASTNAME_INPUT)
    page.assert_element(RegisterPage.EMAIL_INPUT)
    page.assert_element(AdministrationPage.PASSWORD_INPUT)
    page.assert_element(RegisterPage.NEWSLETTER_TUMBLER)


def test_add_new_product(browser, url):
    """Проверка создания и удаления продукта в разделе администратора"""
    page = AdministrationPage(browser)
    browser.get(f"{url}/administration/")
    login = 'user'
    password = 'bitnami'
    page.login(login, password)
    NavigationPanel(browser).go_to_tab('catalog', 'product')
    page.wait_title('Products')
    page = AdminProductPage(browser)
    # Создание продукта
    page.create_product(product_name='New Laptop',
                        meta_tag_title='test_meta_tag_title',
                        model='567',
                        seo='test1')
    NavigationPanel(browser).go_to_tab('catalog', 'product')
    page.set_filter_product_name('New Laptop')
    product_name = page.assert_element((By.XPATH, "//table//tbody//td[3]")).text.split('\n')[0]
    model = page.assert_element((By.XPATH, "//table//tbody//td[4]")).text
    assert product_name == 'New Laptop'
    assert model == '567'
    # Удаление продукта
    page.delete_product('New Laptop')
    page.set_filter_product_name('New Laptop')
    page.assert_element((By.XPATH, "//td[contains(text(), 'No results!')]"))


def test_register_user(browser, url):
    """Проверка регистрации нового пользователя"""
    browser.get(f"{url}/index.php?route=account/register")
    page = RegisterPage(browser)
    page.register_user(first_name='test_user', lastname='test_lastname',
                       email=random_email(), password='123456aQ!')
    page.click(TopPanel.USER_BUTTON)
    page.assert_element(TopPanel.MY_ACCOUNT_ITEM)


@pytest.mark.parametrize('currency', ['€ Euro', '£ Pound Sterling', '$ US Dollar'])
def test_change_currency(browser, currency):
    """Проверка смены валюты"""
    page = TopPanel(browser)
    page.change_currency(currency)
    page.assert_text(TopPanel.CURRENCY_ICON, currency[0])
    prices_new = page.assert_elements(MainPage.PRICE_NEW)
    print(prices_new)
    for price in prices_new:
        if currency == '€ Euro':
            assert price.text[-1] == currency[0]
        else:
            assert price.text[0] == currency[0]
