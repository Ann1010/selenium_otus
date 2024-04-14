import random
import time

import allure
import pytest
from selenium.webdriver.common.by import By

import sys
sys.path.append("..")

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
@allure.feature("Главная страница")
class TestMainPage:

    @allure.title("Проверка отображения основных элементов на странице")
    def test_check_elements(self, browser, url):
        page = MainPage(browser)
        page.open(url)
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

    @allure.title("Проверка смены валюты")
    def test_change_currency(self, browser, url):
        page = MainPage(browser)
        page.open(url)
        current_price_new = page.assert_elements(MainPage.PRICE_NEW)
        current_price_text = [price.text for price in current_price_new]
        TopPanel(browser).change_currency('€ Euro')
        new_price = page.assert_elements(MainPage.PRICE_NEW)
        new_price_text = [price.text for price in new_price]
        for i in range(len(new_price_text)):
            assert current_price_text[i] != new_price_text[i], \
                'При смене валюты не изменилась цена продуктов'

    @pytest.mark.parametrize('currency', ['€ Euro', '£ Pound Sterling', '$ US Dollar'])
    @allure.title("Проверка выбора валюты {currency}")
    def test_choose_currency(self, browser, currency, url):
        """Проверка смены валюты"""
        page = TopPanel(browser)
        page.open(url)
        page.change_currency(currency)
        page.assert_text(TopPanel.CURRENCY_ICON, currency[0])
        prices_new = page.assert_elements(MainPage.PRICE_NEW)
        for price in prices_new:
            if currency == '€ Euro':
                assert price.text[-1] == currency[0]
            else:
                assert price.text[0] == currency[0]

    @allure.title("Проверка добавления продукта в корзину")
    def test_add_product(self, browser, url):
        page = MainPage(browser)
        page.open(url)
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
@allure.feature('Страница Каталог')
class TestCatalogPage:
    @pytest.mark.parametrize('tab', ['desktops', 'laptop-notebook'])
    @allure.title("Проверка отображения основных элементов")
    def test_check_elements(self, browser, url, tab):
        page = CatalogPage(browser)
        page.open(f"{url}/en-gb/catalog/{tab}")
        page.assert_element(CatalogPage.LEFT_MENU)
        page.assert_element(CatalogPage.COMPARE_BUTTON)
        page.assert_element(CatalogPage.INPUT_SORT)

        page.click(CatalogPage.INPUT_LIMIT)
        limits = page.assert_elements(CatalogPage.LIMITS)
        limits_list = ['10', '25', '50', '75', '100']
        for limit in limits:
            assert limit.text in limits_list

    @pytest.mark.parametrize('tab', ['desktops', 'laptop-notebook'])
    @allure.title("Проверка отображения основных элементов")
    def test_change_currency(self, browser, url, tab):
        page = CatalogPage(browser)
        page.open(f"{url}/en-gb/catalog/{tab}")
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
@allure.feature("Страница Продукта")
class TestProductPage:
    @pytest.mark.parametrize('product', ['macbook', 'iphone'])
    @allure.title("Проверка отображения элементов на странице")
    def test_check_product_page(self, browser, url, product):
        page = ProductPage(browser)
        page.open(f"{url}/en-gb/product/{product}")
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
@allure.feature("Страница Входа в админку")
class TestLoginPage:
    @allure.title("Проверка отображения основных элементов на странице")
    def test_check_login_page(self, browser, url):
        page = AdministrationPage(browser)
        page.open(f"{url}/administration/")
        page.assert_element(AdministrationPage.USERNAME_INPUT)
        page.assert_element(AdministrationPage.PASSWORD_INPUT)
        page.assert_element(AdministrationPage.SUBMIT_BUTTON)
        page.assert_text(AdministrationPage.TEXT_LOGIN, 'Please enter your login details.')
        page.click(AdministrationPage.SUBMIT_BUTTON)
        page.assert_element(ProductPage.ALERT_LOGIN_ERROR)

    @allure.title("Проверка входа/выхода из админки")
    def test_login_logout(self, browser, url):
        login = 'user'
        password = 'bitnami'
        page = AdministrationPage(browser)
        page.open(f"{url}/administration/")
        page.input_value(AdministrationPage.USERNAME_INPUT, login)
        page.input_value(AdministrationPage.PASSWORD_INPUT, password)
        page.click(AdministrationPage.SUBMIT_BUTTON)
        page.wait_title('Dashboard')
        page.assert_text(AdministrationPage.PAGE_HEADER, 'Dashboard')
        page.click(AdministrationPage.LOGOUT_BUTTON)
        page.wait_title('Administration')
        page.assert_element(AdministrationPage.USERNAME_INPUT)


@pytest.mark.register
@allure.feature("Страница Регистрация")
class TestRegisterPage:
    @allure.title("Проверка отображения страницы Регистрация пользователя")
    def test_check_register_page(self, browser, url):
        page = RegisterPage(browser)
        page.open(f"{url}/index.php?route=account/register")
        page.assert_element(RegisterPage.FIRST_NAME_INPUT)
        page.assert_element(RegisterPage.LASTNAME_INPUT)
        page.assert_element(RegisterPage.EMAIL_INPUT)
        page.assert_element(AdministrationPage.PASSWORD_INPUT)
        page.assert_element(RegisterPage.NEWSLETTER_TUMBLER)

    @allure.title("Проверка регистрации нового пользователя")
    def test_register_user(self, browser, url):
        page = RegisterPage(browser)
        page.open(f"{url}/index.php?route=account/register")
        page.register_user(first_name='test_user', lastname='test_lastname',
                           email=random_email(), password='123456aQ!')
        page.click(TopPanel.USER_BUTTON)
        page.assert_element(TopPanel.MY_ACCOUNT_ITEM)


@pytest.mark.register
@allure.feature("Админка: работа с продуктами")
class TestAdminProductPage:
    @allure.title("Проверка создания и удаления продукта")
    def test_add_new_product(self, browser, url):
        page = AdministrationPage(browser)
        page.open(f"{url}/administration/")
        login = 'user'
        password = 'bitnami'
        page.login(login, password)
        NavigationPanel(browser).go_to_tab('catalog', 'product')
        page.wait_title('Products')
        page = AdminProductPage(browser)
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
        page.delete_product('New Laptop')
        page.set_filter_product_name('New Laptop')
        page.assert_element((By.XPATH, "//td[contains(text(), 'No results!')]"))
