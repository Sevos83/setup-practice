import pytest
import time
import random
from unittest.mock import patch
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class MockWebDriver:
    """Мок-класс для WebDriver"""

    def __init__(self):
        self.current_url = "https://www.google.com/search?q=mocked"
        self.title = "Mocked Google Search"

    def get(self, url):
        pass

    def find_elements(self, by, value):
        # Возвращаем 7 мокнутых результатов для всех запросов
        return [MockWebElement() for _ in range(7)]

    def save_screenshot(self, path):
        pass


class MockWebElement:
    """Мок-класс для WebElement"""

    def send_keys(self, text):
        pass

    def click(self):
        pass


@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_google_search_mocked(query):
    """Параметризированный тест с мокированием поиска Google"""
    print(f"\nТестируем запрос: '{query}'")

    # 1. Мокируем браузер
    with patch('selenium.webdriver.Chrome') as mock_driver:
        mock_driver.return_value = MockWebDriver()

        # 2. Инициализация мокнутого драйвера
        browser = mock_driver()

        # 3. Переход на Google (мокнутый)
        browser.get("https://www.google.com/ncr")

        # 4. Поиск поля ввода (мокнутый)
        search_box = MockWebElement()

        # 5. Имитация человеческого ввода
        print("  Ввод запроса по буквам...")
        for ch in query:
            search_box.send_keys(ch)
            time.sleep(random.uniform(0.1, 0.25))

        # 6. Отправка запроса
        time.sleep(random.uniform(0.8, 1.2))
        search_box.send_keys(Keys.RETURN)
        print("  Запрос отправлен")

        # 7. Получение результатов (мокнутых)
        results = browser.find_elements(By.CSS_SELECTOR, "div.g")
        print(f"  Найдено результатов: {len(results)}")

        # 8. Проверка количества результатов
        assert len(results) > 5, f"Для запроса '{query}' найдено {len(results)} результатов"

        # 9. Дополнительная проверка URL
        assert "google.com/search" in browser.current_url


if __name__ == "__main__":
    pytest.main(["-v"])