import pytest
from playwright.sync_api import sync_playwright
import time
import random


@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_duckduckgo_search_results(query):
    with sync_playwright() as p:
        # 1. Запускаем браузер
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print(f"\nТестируем запрос: '{query}'")

            # 2. Переходим на DuckDuckGo
            page.goto("https://duckduckgo.com/")

            # 3. Вводим запрос с имитацией человеческого набора
            search_box = page.locator("#searchbox_input")
            search_box.wait_for(state="visible")

            print("  Ввод запроса по буквам...")
            for ch in query:
                search_box.type(ch, delay=random.randint(50, 200))  # Задержка 50-200 мс
                time.sleep(random.uniform(0.1, 0.3))

            # 4. Нажимаем Enter
            search_box.press("Enter")
            print("  Запрос отправлен")

            # 5. Ждем результаты и проверяем их количество
            page.wait_for_selector("article", state="visible")
            results = page.locator("article")
            count = results.count()
            print(f"  Найдено результатов: {count}")

            # 6. Проверяем что результатов больше 5
            assert count > 5, f"Для запроса '{query}' найдено {count} результатов (ожидалось >5)"
            print(f"  Успех: найдено {count} результатов")

        except Exception as e:
            print(f"  Ошибка: {str(e)}")
            page.screenshot(path=f"error_{query}.png")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    pytest.main(["-v"])