import time

import allure
from selenium.webdriver.common.by import By

from ..base_page import BasePage


class AdminProductPage(BasePage):
    NEW_PRODUCT_BUTTON = (By.XPATH, "//a[@title='Add New']")
    PRODUCT_NAME_INPUT = (By.XPATH, "//input[@name='product_description[1][name]']")
    META_TAG_TITLE_INPUT = (By.XPATH, "//input[@name='product_description[1][meta_title]']")
    MODEL_INPUT = (By.XPATH, "//input[@id='input-model']")
    SEO_INPUT = (By.XPATH, "//input[@name='product_seo_url[0][1]']")
    SAVE_BUTTON = (By.XPATH, "//button[@title='Save']")
    FILTER_PRODUCT_NAME_INPUT = (By.XPATH, "//input[@name='filter_name']")
    FILTER_BUTTON = (By.XPATH, "//button[contains(text(), 'Filter')]")
    DELETE_BUTTON = (By.XPATH, "//button[@title='Delete']")

    @allure.step("Переход к вкладке '{tab}' в форме добавления продукта")
    def go_to_tab_add_product(self, tab: str):
        self.assert_element((By.XPATH, f"//ul[@class='nav nav-tabs']//a[contains(text(), '{tab}')]")).click()

    @allure.step("Создание продукта {product_name}")
    def create_product(self, product_name: str,
                       meta_tag_title: str,
                       model: str,
                       seo: str):
        self.click(self.NEW_PRODUCT_BUTTON)
        self.input_value(self.PRODUCT_NAME_INPUT, product_name)
        self.input_value(self.META_TAG_TITLE_INPUT, meta_tag_title)
        self.go_to_tab_add_product('Data')
        self.input_value(self.MODEL_INPUT, model)
        self.go_to_tab_add_product('SEO')
        self.input_value(self.SEO_INPUT, seo)
        self.click(self.SAVE_BUTTON)

    @allure.step("Установка фильтра {product_name}")
    def set_filter_product_name(self, product_name):
        """Установка фильтра"""
        self.input_value(self.FILTER_PRODUCT_NAME_INPUT, product_name)
        self.click((By.XPATH, "//h1"))
        self.click(self.FILTER_BUTTON)
        time.sleep(2)

    @allure.step("Удаление продукта {product_name}")
    def delete_product(self, product_name):
        product_name = self.assert_element((By.XPATH, f"//table//tbody//td[3][contains(text(), '{product_name}')]"))
        row = product_name.find_element(By.XPATH, "ancestor::tr")
        checkbox = row.find_element(By.XPATH, ".//td//input[@type='checkbox']")
        self.set_checkbox(checkbox, True)
        self.click(self.DELETE_BUTTON)
        self.accept_alert()

