import pytest
import time
import random
from unittest.mock import MagicMock
from playwright.sync_api import Page


class MockPlaywrightPage:
    """Мок-класс для Page Playwright"""

    def __init__(self):
        self.url = "https://www.google.com/search?q=mocked"
        self.content = "<html><body><div class='g'>Result 1</div><div class='g'>Result 2</div></body></html>"
        self.locator_cache = {}

    def goto(self, url, timeout=None):
        pass

    def locator(self, selector):
        if selector not in self.locator_cache:
            mock_locator = MagicMock()

            # Мокируем разные селекторы
            if selector == "button:has-text('Accept all')":
                mock_locator.is_visible.return_value = False
            elif selector == "[name=q]":
                mock_locator.type = MagicMock()
                mock_locator.press = MagicMock()
            elif selector == "div.g":
                mock_locator.count.return_value = 7  # Всегда возвращаем 7 результатов
                mock_locator.first.wait_for = MagicMock()

            self.locator_cache[selector] = mock_locator
        return self.locator_cache[selector]

    def screenshot(self, **kwargs):
        pass


@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_google_search_playwright_mocked(query):
    """Параметризированный тест с мокированием Playwright"""
    print(f"\nТестируем запрос: '{query}'")

    # 1. Создаем мок-страницу
    page = MockPlaywrightPage()

    # 2. Переход на Google (мокнутый)
    page.goto("https://www.google.com/ncr")

    # 3. Попытка принять куки (мокнутый)
    try:
        cookie_btn = page.locator("button:has-text('Accept all')")
        if cookie_btn.is_visible(timeout=3000):
            cookie_btn.click()
            print("  Куки приняты")
    except:
        print("  Окно с куками не появилось")

    # 4. Находим поле поиска (мокнутое)
    search_box = page.locator("[name=q]")

    # 5. Имитация человеческого ввода
    print("  Ввод запроса по буквам...")
    for ch in query:
        search_box.type(ch, delay=random.randint(100, 250))
        time.sleep(random.uniform(0.1, 0.25))

    # 6. Отправка запроса
    time.sleep(random.uniform(0.8, 1.2))
    search_box.press("Enter")
    print("  Запрос отправлен")

    # 7. Получаем результаты (мокнутые)
    results = page.locator("div.g")
    results.first.wait_for(timeout=10000)

    count = results.count()
    print(f"  Найдено результатов: {count}")

    # 8. Проверяем количество результатов
    assert count > 5, f"Для запроса '{query}' найдено {count} результатов"

    # 9. Дополнительная проверка
    assert "google.com/search" in page.url


if __name__ == "__main__":
    pytest.main(["-v"])