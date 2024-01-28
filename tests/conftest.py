import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service as SafariService


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--url", "-U", default="http://192.168.0.133")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--drivers", default=os.path.expanduser("~/Downloads/drivers"))


@pytest.fixture()
def url(request):
    return request.config.getoption("--url")

@pytest.fixture()
def browser(request, url):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    drivers = request.config.getoption("--drivers")

    if browser_name == "chrome":
        service = ChromeService()
        options = ChromeOptions()
        if headless:
            options.add_argument("headless=new")
        _browser = webdriver.Chrome(service=service)
    elif browser_name == "firefox":
        service = FirefoxService()
        options = FirefoxOptions()
        if headless:
            options.add_argument("headless")
        _browser = webdriver.Firefox(service=service)
    elif browser_name == "yandex":
        options=webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless=new")
        service = ChromeService(executable_path=os.path.join(drivers, "yandexdriver"))
        options.binary_location = "/usr/bin/yandex-browser"
        _browser = webdriver.Chrome(service=service, options=options)
    elif browser_name == "safari":
        service = SafariService()
        options = SafariOptions()
        if headless:
            options.add_argument("headless=new")
        _browser = webdriver.Safari(service=service)
    else:
        raise Exception('Driver not supported')

    _browser.set_window_size(3200, 5120)
    _browser.get(url)

    yield _browser
    _browser.close()
