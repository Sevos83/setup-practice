from playwright.sync_api import sync_playwright, expect
import time
import config


def test_unsuccessful_login():
    with sync_playwright() as p:
        # Запускаем браузер
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 1. Переходим на страницу авторизации
            page.goto(config.GITHUB_LOGIN_URL)
            print("Страница авторизации открыта")

            # 2. Вводим корректный логин
            page.fill('input[id="login_field"]', config.GITHUB_LOGIN)
            print("Логин введен")
            time.sleep(0.5)

            # 3. Вводим НЕВЕРНЫЙ пароль
            wrong_password = "wrong_password_123"
            page.fill('input[id="password"]', wrong_password)
            print(f"Введен неверный пароль: {wrong_password}")
            time.sleep(0.5)

            # 4. Кликаем кнопку входа
            page.click('input[name="commit"]')
            print("Кнопка Sign in нажата")

            # 5. Проверяем сообщение об ошибке
            error_message = page.locator("div.flash-error:not([hidden])")
            error_message.wait_for(state="visible", timeout=5000)

            # Проверяем текст ошибки
            expected_error = "Incorrect username or password."

            # Проверка части текста (более устойчивый)
            expect(error_message).to_contain_text(expected_error)

            print(f"Сообщение об ошибке отображается: '{expected_error}'")
            print("Тест неуспешной авторизации пройден!")

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            raise e

        finally:
            # Закрываем браузер
            time.sleep(2)
            browser.close()


if __name__ == "__main__":
    test_unsuccessful_login()