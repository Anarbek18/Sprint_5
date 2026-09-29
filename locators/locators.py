from selenium.webdriver.common.by import By


# Header / navigation
LOGIN_REGISTER_BUTTON = (
    By.XPATH, "//button[normalize-space()='Вход и регистрация']"
)
POST_AD_BUTTON = (
    By.XPATH, "//button[normalize-space()='Разместить объявление']"
)
LOGOUT_BUTTON = (
    By.XPATH, "//button[normalize-space()='Выйти']"
)
USER_AVATAR = (
    By.CSS_SELECTOR, "button.circleSmall"
)
USER_NAME = (
    By.CSS_SELECTOR, "h3.profileText.name"
)
USER_NAME_TEXT = (
    By.XPATH, "//h3[contains(@class,'profileText') and contains(@class,'name') and normalize-space()='User.']"
)

# Login / registration modal
NO_ACCOUNT_BUTTON = (
    By.XPATH, "//button[normalize-space()='Нет аккаунта']"
)
ALREADY_HAVE_ACCOUNT_BUTTON = (
    By.XPATH, "//button[normalize-space()='Уже есть аккаунт']"
)

EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='submitPassword']")

LOGIN_SUBMIT = (
    By.XPATH, "//form[.//input[@name='email']]//button[@type='submit' and normalize-space()='Войти']"
)
REGISTER_SUBMIT = (
    By.XPATH, "//form[.//input[@name='submitPassword']]//button[@type='submit' and normalize-space()='Создать аккаунт']"
)

ERROR_TEXT = (
    By.XPATH, "//*[normalize-space()='Ошибка']"
)

# Create advertisement
AD_TITLE_INPUT = (
    By.XPATH, "//input[@placeholder='Название' or @name='title']"
)
AD_DESCRIPTION_INPUT = (
    By.XPATH, "//textarea[@placeholder='Описание товара' or @name='description']"
)
AD_PRICE_INPUT = (
    By.XPATH, "//input[@placeholder='Стоимость' or @name='price']"
)

# Dropdowns. The HTML supplied with the task uses name="category" and name="city".
AD_CATEGORY_INPUT = (
    By.CSS_SELECTOR, "input[name='category']"
)
AD_CITY_INPUT = (
    By.CSS_SELECTOR, "input[name='city']"
)

# Generic dropdown option by visible text
def dropdown_option(text: str):
    return (
        By.XPATH,
        f"//button[.//span[normalize-space()='{text}'] or normalize-space()='{text}']"
    )


# The task asks to select a condition via RadioButton.
# Prefer a real radio input; fallback in test is the first label containing a radio.
CONDITION_RADIO = (
    By.CSS_SELECTOR, "input[type='radio']"
)

PUBLISH_BUTTON = (
    By.XPATH, "//button[normalize-space()='Опубликовать']"
)

MY_ADS_HEADING = (
    By.XPATH, "//*[normalize-space()='Мои объявления']"
)



def invalid_field_container(field_name):
    return (
        By.XPATH,
        f"//input[@name='{field_name}']/ancestor::div[contains(@class,'input_inputDefault')][1]"
    )

# Dynamic locators
UNAUTHORIZED_MODAL_HEADING = (
    By.XPATH,
    "//*[normalize-space()='Чтобы разместить объявление, авторизуйтесь']"
)


def ad_title(text: str):
    return (
        By.XPATH,
        f"//*[normalize-space()='{text}']"
    )

