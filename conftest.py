import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://qa-desk.education-services.ru/")


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(30)

    try:
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def base_url():
    return BASE_URL
