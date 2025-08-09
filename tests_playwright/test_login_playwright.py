from playwright.sync_api import sync_playwright, expect
import time
import config  # Импортируем наш конфигурационный файл


def test_successful_login():
    # Инициализируем Playwright
    with sync_playwright() as p:
        # Запускаем браузер
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 1. Переходим на страницу логина
            page.goto(config.GITHUB_LOGIN_URL)
            print("Открыта страница авторизации")

            # 2. Заполняем логин
            page.fill('input[id="login_field"]', config.GITHUB_LOGIN)
            print("Логин введен")
            time.sleep(1)

            # 3. Заполняем пароль
            page.fill('input[id="password"]', config.GITHUB_PASSWORD)
            print("Пароль введен")
            time.sleep(1)

            # 4. Кликаем кнопку входа
            page.click('input[name="commit"]')
            print("Нажата кнопка Sign in")

            # 5. Проверяем успешную авторизацию
            # Ждем появления аватара пользователя
            avatar = page.locator('[class*="avatar-user"]').first
            avatar.wait_for(state="visible", timeout=1000)
            expect(avatar).to_be_visible()
            print("Успешная авторизация! Аватар пользователя отображается")

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            raise e

        finally:
            time.sleep(2)
            browser.close()


if __name__ == "__main__":
    test_successful_login()