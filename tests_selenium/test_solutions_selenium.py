import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

FIRST_NAME = "Иван"
LAST_NAME = "Петров"


class GitHubPages:
    """Page Object модель для работы со страницами GitHub"""

    def __init__(self, driver):
        self.driver = driver

        # Определение локаторов для элементов страницы:
        self.solutions_menu = (By.XPATH, "//button[contains(text(),'Solutions')]")
        self.ci_cd_option = (By.XPATH, "//a[contains(text(),'CI/CD') and @href]")
        self.contact_sales_btn = (By.XPATH, "//span[text()='Contact sales']")
        self.first_name_input = (By.CSS_SELECTOR, "input[name='first_name']")
        self.last_name_input = (By.CSS_SELECTOR, "input[name='last_name']")

    def go_to_homepage(self):
        """Переход на главную страницу GitHub"""
        # Открытие URL главной страницы GitHub
        self.driver.get("https://github.com/")
        # Опциональное разворачивание окна на весь экран
        # self.driver.maximize_window()

    def open_ci_cd_page(self):
        """Открытие страницы CI/CD через меню Solutions"""
        # Вывод сообщения в консоль о текущем действии
        print("Открытие меню Solutions")

        # Ожидание появления и доступности меню Solutions
        solutions = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.solutions_menu)
        )

        # Наведение курсора мыши на меню Solutions для отображения выпадающего списка
        ActionChains(self.driver).move_to_element(solutions).perform()

        print("Выбор пункта CI/CD")
        # Ожидание появления пункта CI/CD в выпадающем меню
        ci_cd = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ci_cd_option)
        )
        # Клик по пункту CI/CD
        ci_cd.click()

    def open_contact_form(self):
        """Открытие формы 'Contact sales'"""
        print("Нажатие кнопки Contact sales")
        # Ожидание появления кнопки "Contact sales" и проверка, что она кликабельна
        contact_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.contact_sales_btn)
        )
        # Клик по кнопке "Contact sales"
        contact_btn.click()

    def fill_contact_form(self):
        """Заполнение полей формы 'First name' и 'Last name'"""
        # Ожидание появления поля для ввода имени
        first_name = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.first_name_input)
        )
        # Ввод тестового имени в поле First name
        first_name.send_keys(FIRST_NAME)

        # Ожидание появления поля для ввода фамилии
        last_name = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.last_name_input)
        )
        # Ввод тестовой фамилии в поле Last name
        last_name.send_keys(LAST_NAME)

    def verify_form_data(self):
        """Проверка введенных данных в форме"""
        # Получение значения из поля First name после ввода
        actual_first_name = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.first_name_input)
        ).get_attribute("value")  # Извлечение значения атрибута 'value'

        # Получение значения из поля Last name после ввода
        actual_last_name = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.last_name_input)
        ).get_attribute("value")  # Извлечение значения атрибута 'value'

        # Возврат фактических значений для последующей проверки
        return actual_first_name, actual_last_name


class GitHubContactSalesTest(unittest.TestCase):
    """Тест-кейс для проверки формы Contact Sales на GitHub"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        # Инициализация драйвера Chrome
        self.driver = webdriver.Chrome()
        # Создание экземпляра Page Object для работы со страницами GitHub
        self.github = GitHubPages(self.driver)
        # Переход на главную страницу GitHub
        self.github.go_to_homepage()
        time.sleep(1)

    def test_contact_form_submission(self):
        """Основной тест: проверка заполнения и данных формы контактов"""
        # Вызов метода для открытия страницы CI/CD
        self.github.open_ci_cd_page()
        time.sleep(1)

        print("Открытие формы контактов")
        # Вызов метода для открытия формы "Contact sales"
        self.github.open_contact_form()
        time.sleep(2)

        print("Заполнение формы")
        self.github.fill_contact_form()
        time.sleep(1)

        # Получение фактических значений из формы
        actual_first, actual_last = self.github.verify_form_data()

        # Проверка соответствия фактических и ожидаемых значений:
        self.assertEqual(actual_first, FIRST_NAME)
        self.assertEqual(actual_last, LAST_NAME)

        print("Проверка пройдена: данные корректны!")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    # Запуск всех тестов, определенных в классе
    unittest.main()