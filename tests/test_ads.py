import os

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.locators import (
    LOGIN_REGISTER_BUTTON,
    EMAIL_INPUT,
    PASSWORD_INPUT,
    LOGIN_SUBMIT,
    POST_AD_BUTTON,
    AD_TITLE_INPUT,
    AD_DESCRIPTION_INPUT,
    AD_PRICE_INPUT,
    AD_CATEGORY_INPUT,
    AD_CITY_INPUT,
    CONDITION_RADIO,
    PUBLISH_BUTTON,
    MY_ADS_HEADING,
    USER_NAME,
    UNAUTHORIZED_MODAL_HEADING,
    ad_title,
    dropdown_option,
)


WAIT = 10


def wait_visible(driver, locator):
    return WebDriverWait(driver, WAIT).until(
        EC.visibility_of_element_located(locator)
    )


def wait_click(driver, locator):
    WebDriverWait(driver, WAIT).until(
        EC.element_to_be_clickable(locator)
    ).click()


def login(driver, base_url):
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")

    if not email or not password or password == "CHANGE_ME":
        pytest.skip("Set TEST_USER_EMAIL and TEST_USER_PASSWORD in .env")

    driver.get(base_url)
    wait_click(driver, LOGIN_REGISTER_BUTTON)
    wait_visible(driver, EMAIL_INPUT).send_keys(email)
    driver.find_element(*PASSWORD_INPUT).send_keys(password)
    wait_click(driver, LOGIN_SUBMIT)
    wait_visible(driver, USER_NAME)


def select_dropdown(driver, input_locator, option_text):
    wait_click(driver, input_locator)
    wait_click(driver, dropdown_option(option_text))


class TestAds:

    def test_create_ad_unauthorized(self, driver, base_url):
        driver.get(base_url)
        wait_click(driver, POST_AD_BUTTON)

        assert wait_visible(
            driver, UNAUTHORIZED_MODAL_HEADING
        ).is_displayed()

    def test_create_ad_authorized(self, driver, base_url):
        title = "Автотестовое объявление Selenium"

        login(driver, base_url)
        wait_click(driver, POST_AD_BUTTON)

        wait_visible(driver, AD_TITLE_INPUT).send_keys(title)
        wait_visible(driver, AD_DESCRIPTION_INPUT).send_keys(
            "Описание товара, созданное UI-автотестом."
        )
        wait_visible(driver, AD_PRICE_INPUT).send_keys("15000")

        select_dropdown(driver, AD_CATEGORY_INPUT, "Технологии")
        select_dropdown(driver, AD_CITY_INPUT, "Москва")

        radio = WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(CONDITION_RADIO)
        )
        driver.execute_script("arguments[0].click();", radio)

        wait_click(driver, PUBLISH_BUTTON)

        wait_click(driver, USER_NAME)
        wait_visible(driver, MY_ADS_HEADING)

        assert wait_visible(driver, ad_title(title)).is_displayed()
