from playwright.sync_api import sync_playwright, expect


class GitHubTopics:
    def __init__(self, page):
        self.page = page

        # Локаторы
        self.resources_menu = "button:has-text('Resources')"
        self.topics_heading = "span#resources-topics-heading"
        self.topic_links = "xpath=//span[@id='resources-topics-heading']/following-sibling::ul//a"

        # Ожидаемые темы
        self.expected_topics = ["AI", "DevOps", "Security", "Software Development", "View all"]

    def go_to_homepage(self):
        self.page.goto("https://github.com/")
        self.page.wait_for_load_state("load")

    def clean_text(self, text):
        """Очистка текста от лишних пробелов и символов"""
        return text.strip().replace('\n', '')

    def open_and_check_resources(self):
        """2. Открыть Resources и проверить темы"""
        # Наводим на кнопку Resources
        self.page.locator(self.resources_menu).hover()

        # Ждем появления заголовка Topics
        self.page.locator(self.topics_heading).wait_for(state="visible", timeout=5000)
        print("Меню Resources открыто, раздел Topics найден")

        # Получаем и очищаем тексты ссылок
        topics = self.page.locator(self.topic_links)
        topic_texts = [self.clean_text(text) for text in topics.all_text_contents()]

        # Проверяем наличие всех ожидаемых тем
        for topic in self.expected_topics:
            assert topic in topic_texts, f"Тема '{topic}' не найдена"
            print(f"✓ Найдена тема: {topic}")

        print("Все темы присутствуют!")


def test_github_topics():
    with sync_playwright() as p:
        print("\n=== Тест: Проверка тем GitHub ===")

        # Настройки браузера
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            test = GitHubTopics(page)

            # 1. Переход на GitHub
            test.go_to_homepage()

            # 2. Проверка меню Resources
            test.open_and_check_resources()

            print("\nТест успешно завершен!")

        except Exception as e:
            print(f"\nОШИБКА: {e}")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_github_topics()