import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def test_successful_login():
    # Инициализация драйвера с автоматическим управлением
    driver = webdriver.Chrome()

    try:
        # 1. Открываем страницу авторизации
        driver.get(config.GITHUB_LOGIN_URL)
        print("Страница авторизации открыта")

        # 2. Вводим логин
        login_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login_field")))
        login_field.send_keys(config.GITHUB_LOGIN)
        print("Логин введен")
        time.sleep(1)

        # 3. Вводим пароль
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(config.GITHUB_PASSWORD)
        print("Пароль введен")
        time.sleep(1)

        # 4. Нажимаем кнопку входа
        signin_button = driver.find_element(By.NAME, "commit")
        signin_button.click()
        print("Кнопка Sign in нажата")

        # 5. Проверяем успешную авторизацию по аватару
        avatar = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[class*="avatar-user"]')))

        print("Аватар пользователя отображается")
        print("Успешная авторизация!")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        raise e

    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    test_successful_login()