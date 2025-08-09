import pytest
import time
import random
from playwright.sync_api import sync_playwright, expect


def human_type(page, selector, text):
    """Имитация человеческого ввода"""
    for i, char in enumerate(text):
        page.type(selector, char, delay=random.randint(50, 150))
        if i % 3 == 0:
            time.sleep(random.uniform(0.2, 0.4))


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        # Настройка браузера с защитой от детекции
        browser = p.chromium.launch(
            headless=False,
            slow_mo=100,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        yield page
        browser.close()


@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_google_search_playwright(browser, query):
    """Тест поиска Google через Playwright"""
    print(f"\nТестируем запрос: '{query}'")

    try:
        # 1. Переход на Google
        browser.goto("https://www.google.com/ncr", timeout=15000)
        time.sleep(random.uniform(2, 4))

        # 2. Проверка CAPTCHA
        if "sorry" in browser.url:
            pytest.skip(f"CAPTCHA обнаружена при входе для '{query}'")

        # 3. Принятие куки (несколько вариантов селекторов)
        cookie_selectors = [
            "button:has-text('Accept all')",
            "button:has-text('I agree')",
            "button:has-text('Accept') >> visible=true"
        ]

        for selector in cookie_selectors:
            try:
                browser.locator(selector).click(timeout=3000)
                print("  Куки приняты")
                time.sleep(1)
                break
            except:
                continue
        else:
            print("  Окно с куками не появилось")

        # 4. Поиск поля ввода
        search_selectors = [
            "textarea[name='q']",
            "input[name='q']",
            "[name='q']",
            "[type='search']"
        ]

        search_box = None
        for selector in search_selectors:
            if browser.locator(selector).count() > 0:
                search_box = browser.locator(selector)
                break

        if not search_box:
            browser.screenshot(path="search_box_not_found.png")
            pytest.fail("Не удалось найти поле поиска")

        # 5. Человекообразный ввод
        print("  Имитируем человеческий ввод...")
        search_box.click()
        human_type(browser, search_selectors[0], query)

        # 6. Отправка запроса
        time.sleep(random.uniform(0.8, 1.5))
        browser.keyboard.press("Enter")
        print("  Запрос отправлен")
        time.sleep(random.uniform(2, 4))

        # 7. Проверка CAPTCHA после поиска
        if "sorry" in browser.url:
            pytest.skip(f"CAPTCHA после поиска для '{query}'")

        # 8. Поиск результатов (несколько стратегий)
        result_selectors = [
            "div.g",  # Классические результаты
            "div[data-snf]",  # Новый формат
            "h3 >> visible=true",  # Заголовки
            "a >> h3"  # Ссылки с заголовками
        ]

        results = None
        for selector in result_selectors:
            if browser.locator(selector).count() > 3:
                results = browser.locator(selector)
                break

        if not results:
            browser.screenshot(path=f"no_results_{query}.png")
            pytest.fail(f"Не найдены результаты для '{query}'")

        count = results.count()
        print(f"  Найдено результатов: {count}")

        # 9. Проверка количества результатов
        assert count > 5, f"Мало результатов ({count}) для '{query}'"

    except Exception as e:
        browser.screenshot(path=f"error_{query}.png", full_page=True)
        print(f"  Ошибка: {str(e)}")
        raise