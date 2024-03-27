import os
import random

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
    parser.addoption("--bv",  default="91.0")
    parser.addoption("--executor", action="store", default="127.0.0.1")
    parser.addoption("--drivers", default=os.path.expanduser("~/Downloads/drivers"))
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--video", action="store_true")
    parser.addoption("--logs", action="store_true")
    

@pytest.fixture()
def url(request):
    return request.config.getoption("--url")

@pytest.fixture()
def browser(request, url):
    browser_name = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    headless = request.config.getoption("--headless")
    drivers = request.config.getoption("--drivers")
    version = request.config.getoption("--bv")
    vnc = request.config.getoption("--vnc")
    video = request.config.getoption("--video")
    logs = request.config.getoption("--logs")

    executor_url = f"http://{executor}:4444/wd/hub"

    if browser_name == "chrome":
        service = ChromeService()
        options = ChromeOptions()
        if headless:
            options.add_argument("headless=new")
        # _browser = webdriver.Chrome(service=service)
    elif browser_name == "firefox":
        service = FirefoxService()
        options = FirefoxOptions()
        if headless:
            options.add_argument("headless")
        # _browser = webdriver.Firefox(service=service)
    elif browser_name == "yandex":
        options=webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless=new")
        service = ChromeService(executable_path=os.path.join(drivers, "yandexdriver"))
        options.binary_location = "/usr/bin/yandex-browser"
        # _browser = webdriver.Chrome(service=service, options=options)
    elif browser_name == "safari":
        service = SafariService()
        options = SafariOptions()
        if headless:
            options.add_argument("headless=new")
        #_browser = webdriver.Safari(service=service)
    else:
        raise Exception('Driver not supported')
    
    caps = {
        "browserName": browser_name,
        "browserVersion": version,
        "selenoid:options": {
            "enableVNC": vnc,
            "name": os.getenv("BUILD_NUMBER", str(random.randint(9000, 10000))),
            "screenResolution": "1280x2000",
            "enableVideo": video,
            "enableLog": logs,
            "timeZone": "Europe/Moscow",
            "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"]

        },
        "acceptInsecureCerts": True,
    }
    
    for k, v in caps.items():
        options.set_capability(k, v)
        print(k, v)

    driver = webdriver.Remote(
        command_executor=executor_url,
        options=options
    )

    driver.set_window_size(3200, 5120)
    driver.get(url)

    yield driver
    driver.close()
