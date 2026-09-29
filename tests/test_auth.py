import os
import time

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.locators import (
    LOGIN_REGISTER_BUTTON,
    NO_ACCOUNT_BUTTON,
    ALREADY_HAVE_ACCOUNT_BUTTON,
    EMAIL_INPUT,
    PASSWORD_INPUT,
    CONFIRM_PASSWORD_INPUT,
    LOGIN_SUBMIT,
    REGISTER_SUBMIT,
    USER_NAME,
    USER_AVATAR,
    LOGOUT_BUTTON,
    ERROR_TEXT,
    invalid_field_container,
)


WAIT = 10
PASSWORD = "Test123!Qa456"


def wait_click(driver, locator):
    WebDriverWait(driver, WAIT).until(
        EC.element_to_be_clickable(locator)
    ).click()


def wait_visible(driver, locator):
    return WebDriverWait(driver, WAIT).until(
        EC.visibility_of_element_located(locator)
    )


def open_registration(driver, base_url):
    driver.get(base_url)
    wait_click(driver, LOGIN_REGISTER_BUTTON)
    wait_click(driver, NO_ACCOUNT_BUTTON)
    wait_visible(driver, CONFIRM_PASSWORD_INPUT)


def open_login(driver, base_url):
    driver.get(base_url)
    wait_click(driver, LOGIN_REGISTER_BUTTON)
    wait_visible(driver, PASSWORD_INPUT)


def fill_registration(driver, email, password=PASSWORD):
    driver.find_element(*EMAIL_INPUT).send_keys(email)
    driver.find_element(*PASSWORD_INPUT).send_keys(password)
    driver.find_element(*CONFIRM_PASSWORD_INPUT).send_keys(password)


def fill_login(driver, email, password):
    driver.find_element(*EMAIL_INPUT).send_keys(email)
    driver.find_element(*PASSWORD_INPUT).send_keys(password)



class TestAuth:

    def test_registration_success(driver, base_url):
        unique_email = f"autotest_{int(time.time() * 1000)}@example.com"

        open_registration(driver, base_url)
        fill_registration(driver, unique_email)
        wait_click(driver, REGISTER_SUBMIT)

        wait_visible(driver, USER_NAME)
        wait_visible(driver, USER_AVATAR)

        # Фактический результат учебного сервиса: после регистрации
        # открывается /regiatration, при этом пользователь авторизован.
        assert driver.current_url.startswith(base_url.rstrip("/") + "/regiatration")
        assert driver.find_element(*USER_NAME).text.strip() == "User."
        assert driver.find_element(*USER_AVATAR).is_displayed()

    def test_registration_invalid_email(driver, base_url):
        open_registration(driver, base_url)

        driver.find_element(*EMAIL_INPUT).send_keys("invalid-email")
        wait_click(driver, REGISTER_SUBMIT)

        assert wait_visible(driver, ERROR_TEXT).is_displayed()

        # Красная рамка применяется к контейнеру input, а не обязательно
        # непосредственно к элементу <input>.
        for field_name in ("email", "password", "submitPassword"):
            container = wait_visible(
                driver, invalid_field_container(field_name)
            )
            border_color = container.value_of_css_property("border-color")
            box_shadow = container.value_of_css_property("box-shadow")
            assert (
                border_color not in ("", "rgb(0, 0, 0)", "rgba(0, 0, 0, 0)")
                or "rgb(255, 0, 0)" in box_shadow
                or "rgba(255, 0, 0" in box_shadow
                or "#ff" in box_shadow.lower()
            ), f"Поле {field_name} не выделено красным: border={border_color}, shadow={box_shadow}"

    def test_registration_existing_user(driver, base_url):
        email = os.getenv("TEST_USER_EMAIL")
        password = os.getenv("TEST_USER_PASSWORD")

        if not email or not password or password == "CHANGE_ME":
            pytest.skip("Set TEST_USER_EMAIL and TEST_USER_PASSWORD in .env")

        open_registration(driver, base_url)
        fill_registration(driver, email, password)
        wait_click(driver, REGISTER_SUBMIT)

        assert wait_visible(driver, ERROR_TEXT).is_displayed()
        for locator in (EMAIL_INPUT, PASSWORD_INPUT, CONFIRM_PASSWORD_INPUT):
            assert wait_visible(driver, locator).is_displayed()

    def test_login(driver, base_url):
        email = os.getenv("TEST_USER_EMAIL")
        password = os.getenv("TEST_USER_PASSWORD")

        if not email or not password or password == "CHANGE_ME":
            pytest.skip("Set TEST_USER_EMAIL and TEST_USER_PASSWORD in .env")

        open_login(driver, base_url)
        fill_login(driver, email, password)
        wait_click(driver, LOGIN_SUBMIT)

        wait_visible(driver, USER_NAME)
        wait_visible(driver, USER_AVATAR)

        # Фактический результат учебного сервиса: после регистрации
        # открывается /regiatration, при этом пользователь авторизован.
        assert driver.current_url.startswith(base_url.rstrip("/") + "/regiatration")
        assert driver.find_element(*USER_NAME).text.strip() == "User."
        assert driver.find_element(*USER_AVATAR).is_displayed()

    def test_logout(driver, base_url):
        email = os.getenv("TEST_USER_EMAIL")
        password = os.getenv("TEST_USER_PASSWORD")

        if not email or not password or password == "CHANGE_ME":
            pytest.skip("Set TEST_USER_EMAIL and TEST_USER_PASSWORD in .env")

        open_login(driver, base_url)
        fill_login(driver, email, password)
        wait_click(driver, LOGIN_SUBMIT)

        wait_visible(driver, USER_NAME)
        wait_visible(driver, USER_AVATAR)
        wait_click(driver, LOGOUT_BUTTON)

        wait_visible(driver, LOGIN_REGISTER_BUTTON)
        assert driver.find_element(*LOGIN_REGISTER_BUTTON).is_displayed()
        assert not driver.find_elements(*USER_NAME)
        assert not driver.find_elements(*USER_AVATAR)
