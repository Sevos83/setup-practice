import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def test_unsuccessful_login():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    try:
        # 1. Открываем страницу авторизации
        driver.get(config.GITHUB_LOGIN_URL)
        print("Страница авторизации открыта")

        # 2. Вводим корректный логин
        login_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login_field")))
        login_field.send_keys(config.GITHUB_LOGIN)
        print("Логин введен")
        time.sleep(1)

        # 3. Вводим НЕВЕРНЫЙ пароль
        wrong_password = "wrong_password_123"
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(wrong_password)
        print(f"Введен неверный пароль: {wrong_password}")
        time.sleep(1)

        # 4. Нажимаем кнопку входа
        signin_button = driver.find_element(By.NAME, "commit")
        signin_button.click()
        print("Кнопка Sign in нажата")

        # 5. Проверяем сообщение об ошибке
        # Ждем появления сообщения об ошибке
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.flash-error")))

        # Проверяем текст ошибки
        expected_error = "Incorrect username or password."
        assert expected_error in error_message.text
        print(f"Сообщение об ошибке отображается: '{expected_error}'")

        print("Тест неуспешной авторизации пройден!")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        raise e

    finally:
        # Закрываем браузер
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    test_unsuccessful_login()