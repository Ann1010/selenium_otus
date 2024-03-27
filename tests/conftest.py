import datetime
import logging
import os
import time

import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service as SafariService


def pytest_addoption(parser):
    parser.addoption("--browser_name", default="chrome")
    parser.addoption("--url", "-U", default="http://192.168.0.133")
    parser.addoption("--mobile", action="store_true", default=False)
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--video", action="store_true", default=False)
    parser.addoption("--bv", default="121.0")
    parser.addoption("--executor", action="store", default="192.168.0.133")
    parser.addoption("--log_level", action="store", default="DEBUG")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--drivers", default=os.path.expanduser("~/Downloads/drivers"))


@allure.step("Waiting for availability {url}")
def wait_url_data(url, timeout=10):
    """Метод ожидания доступности урла"""
    while timeout:
        response = requests.get(url)
        if not response.ok:
            time.sleep(1)
            timeout -= 1
        else:
            if "video" in url:
                return response.content
            else:
                return response.text
    return None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != "passed":
        item.status = "failed"
    else:
        item.status = "passed"


@pytest.fixture()
def url(request):
    return request.config.getoption("--url")


@pytest.fixture()
def browser(request, url):
    browser_name = request.config.getoption("--browser_name")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    version = request.config.getoption("--bv")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--video")
    mobile = request.config.getoption("--mobile")
    headless = request.config.getoption("--headless")
    drivers = request.config.getoption("--drivers")
    log_level = request.config.getoption("--log_level")

    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    if executor == "local":
        caps = {"goog:chromeOption": {}}

        if mobile:
            caps["goog:chromeOptions"]["mobileEmulation"] = {
                "deviceName": "iPhone 5/SE"
            }

        if browser_name == "chrome":
            service = ChromeService()
            options = ChromeOptions()
            if headless:
                options.add_argument("headless=new")
                options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(service=service)
        elif browser_name == "firefox":
            service = FirefoxService()
            options = FirefoxOptions()
            if headless:
                options.add_argument("headless")
            driver = webdriver.Firefox(service=service)
        elif browser_name == "yandex":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("headless=new")
            service = ChromeService(executable_path=os.path.join(drivers, "yandexdriver"))
            options.binary_location = "/usr/bin/yandex-browser"
            driver = webdriver.Chrome(service=service, options=options)
        elif browser_name == "safari":
            service = SafariService()
            options = SafariOptions()
            if headless:
                options.add_argument("headless=new")
            driver = webdriver.Safari(service=service)
        else:
            raise Exception('Driver not supported')

        driver.set_window_size(3200, 5120)
    else:
        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("headless=new")
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("headless")
        elif browser_name == "yandex":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("headless=new")
            options.binary_location = "/usr/bin/yandex-browser"
        elif browser_name == "safari":
            options = SafariOptions()
            if headless:
                options.add_argument("headless=new")
        else:
            raise Exception('Driver not supported')
        executor_url = f"http://{executor}:4444/wd/hub"

        caps = {
            "browserName": browser_name,
            "browserVersion": version,
            "selenoid:options": {
                "enableVideo": video,
                "enableLog": logs,
                "enableVNC": vnc,
                "timeZone": "Europe/Moscow",
                "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"]
            }
        }

        for k, v in caps.items():
            options.set_capability(k, v)

        driver = webdriver.Remote(
            command_executor=executor_url,
            options=options
        )

    if not mobile:
        driver.maximize_window()

    logger.info("===> Test %s started at %s" % (request.node.name, datetime.datetime.now()))

    driver.log_level = log_level
    driver.logger = logger
    driver.test_name = request.node.name

    logger.info("Browser %s started" % driver)

    def finalizer():
        video_url = f"http://{executor}:8080/video/{driver.session_id}.mp4"

        if request.node.status == "failed":
            if video:
                allure.attach(
                    body=wait_url_data(video_url),
                    name="video_for_" + driver.session_id,
                    attachment_type=allure.attachment_type.MP4,
                )

        if video and wait_url_data(video_url):
            requests.delete(url=video_url)

        driver.quit()

    request.addfinalizer(finalizer)
    return driver
