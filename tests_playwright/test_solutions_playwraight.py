from playwright.sync_api import sync_playwright, expect

# Константы с тестовыми данными
FIRST_NAME = "Иван"
LAST_NAME = "Петров"


class GitHubPages:
    def __init__(self, page):
        self.page = page

        # Локаторы элементов
        self.solutions_menu = "button:has-text('Solutions')"
        self.ci_cd_option = "a:has-text('CI/CD')"
        self.contact_sales_btn = "a:has-text('Contact sales')"

        # Локаторы полей формы
        self.first_name_field = "#form-field-first_name"
        self.last_name_field = "#form-field-last_name"

    def go_to_homepage(self):
        """1. Перейти на главную страницу GitHub"""
        print("Переход на GitHub.com")
        self.page.goto("https://github.com/")
        self.page.wait_for_load_state("load")

    def open_solutions_menu(self):
        """2. Открыть меню Solutions"""
        print("Открытие меню Solutions")
        self.page.locator(self.solutions_menu).hover()
        self.page.wait_for_timeout(500)

    def select_ci_cd(self):
        """3. Выбрать пункт CI/CD"""
        print("Выбор пункта CI/CD")
        with self.page.expect_navigation():
            self.page.locator(self.ci_cd_option).click()

    def click_contact_sales(self):
        """4. Нажать кнопку Contact sales"""
        print("Нажатие кнопки Contact sales")
        self.page.locator(self.contact_sales_btn).first.click()
        self.page.wait_for_load_state("networkidle")

    def fill_contact_form(self):
        """5. Заполнить форму"""
        print("Заполнение формы")
        self.page.locator(self.first_name_field).fill(FIRST_NAME)
        self.page.locator(self.last_name_field).fill(LAST_NAME)

    def verify_form_data(self):
        """6. Проверить заполненные данные"""
        expect(self.page.locator(self.first_name_field)).to_have_value(FIRST_NAME)
        expect(self.page.locator(self.last_name_field)).to_have_value(LAST_NAME)
        print("Проверка пройдена: данные корректны!")


def test_github_contact_sales():
    with sync_playwright() as p:
        print("\nЗапуск теста: GitHub Contact Sales Form")
        print("=====================================")

        # Запускаем браузер
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            github = GitHubPages(page)

            # 1. Переходим на GitHub
            github.go_to_homepage()

            # 2. Открываем меню Solutions
            github.open_solutions_menu()

            # 3. Выбираем CI/CD
            github.select_ci_cd()

            # 4. Нажимаем Contact sales
            github.click_contact_sales()

            # 5. Заполняем форму
            github.fill_contact_form()

            # 6. Проверяем данные
            github.verify_form_data()
            print("\nТест успешно завершен!")
            print("=====================================")

        except Exception as e:
            print("Тест завершен с ошибками")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_github_contact_sales()