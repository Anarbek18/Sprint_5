# Sprint_5 — UI autotests for QA Desk

Учебный проект на Python + Selenium + pytest.

## 1. Установка

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Нужен установленный Google Chrome. Selenium 4 использует Selenium Manager для подбора ChromeDriver.

## 2. Настройка пользователя

Скопируй `.env.example` в `.env` и укажи заранее созданного пользователя:

```env
BASE_URL=https://qa-desk.education-services.ru/
TEST_USER_EMAIL=your_existing_user@example.com
TEST_USER_PASSWORD=your_password
```

Пароль существующего пользователя специально не зашит в проект.

## 3. Запуск

Все тесты:

```bash
pytest -v
```

Только авторизация:

```bash
pytest -v tests/test_auth.py
```

Объявления:

```bash
pytest -v tests/test_ads.py
```

## Структура

```text
Sprint_5/
├── locators/
│   ├── __init__.py
│   └── locators.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_ads.py
├── conftest.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Важные решения

- Каждый тест получает отдельный WebDriver через fixture с `scope="function"`.
- В конце каждого теста браузер закрывается через `driver.quit()` в `finally`.
- Локаторы вынесены в `locators/locators.py`.
- Используются explicit waits, а не `time.sleep()`.
- Для регистрации создаётся уникальный email, чтобы тест не зависел от состояния базы.
- Тест существующего пользователя использует `TEST_USER_EMAIL` и `TEST_USER_PASSWORD`.

## Локаторы по предоставленному HTML

В авторизованном header:
- аватар: `button.circleSmall`;
- имя пользователя: `h3.profileText.name`, текст `User.`;
- выход: `button.btnSmall` внутри блока профиля с текстом `Выйти`;
- публикация: кнопка `Разместить объявление`.

Для формы входа:
- Email: `input[name='email']`;
- пароль: `input[name='password']`;
- вход: submit-кнопка с текстом `Войти`;
- переход к регистрации: `Нет аккаунта`.
