from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class GitHubTopics:
    def __init__(self, driver):
        self.driver = driver

        # Локаторы
        self.resources_menu = (By.XPATH, "//button[contains(., 'Resources')]")
        self.topics_heading = (By.ID, "resources-topics-heading")
        self.topic_links = (By.XPATH, "//span[@id='resources-topics-heading']/following-sibling::ul//a")

        # Ожидаемые темы
        self.expected_topics = ["AI", "DevOps", "Security", "Software Development", "View all"]

    def go_to_homepage(self):
        """1. Перейти на GitHub"""
        self.driver.get("https://github.com/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    def clean_text(self, text):
        """Очистка текста от лишних пробелов и символов"""
        return text.strip().replace('\n', '')

    def open_and_check_resources(self):
        """2. Открыть Resources и проверить темы"""
        # Наводим на кнопку Resources
        resources = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.resources_menu)
        )
        ActionChains(self.driver).move_to_element(resources).perform()

        # Ждем появления заголовка Topics
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.topics_heading)
        )
        print("Меню Resources открыто, раздел Topics найден")

        # Получаем и очищаем тексты ссылок
        topics = self.driver.find_elements(*self.topic_links)
        topic_texts = [self.clean_text(topic.text) for topic in topics]

        # Проверяем наличие всех ожидаемых тем
        for topic in self.expected_topics:
            assert topic in topic_texts, f"Тема '{topic}' не найдена"
            print(f"✓ Найдена тема: {topic}")

        print("Все темы присутствуют!")


def test_github_topics():
    print("\n=== Тест: Проверка тем GitHub (Selenium) ===")

    # Настройка драйвера
    driver = webdriver.Chrome()

    try:
        test = GitHubTopics(driver)

        # 1. Переход на GitHub
        test.go_to_homepage()

        # 2. Проверка меню Resources
        test.open_and_check_resources()
        print("\nТест успешно завершен!")

    except Exception as e:
        print(f"\nОШИБКА: {e}")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    test_github_topics()