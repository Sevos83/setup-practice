import pytest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture(scope="module")
def browser():
    # Настройка браузера для обхода блокировок
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    yield driver
    driver.quit()


def human_type(element, text):
    """Имитация человеческого ввода с случайными задержками"""
    for i, char in enumerate(text):
        element.send_keys(char)
        if i % 3 == 0:
            time.sleep(random.uniform(0.2, 0.4))
        else:
            time.sleep(random.uniform(0.1, 0.25))


@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_google_search(browser, query):
    """Улучшенный тест поиска Google с обработкой всех сценариев"""
    print(f"\nТестируем запрос: '{query}'")

    try:
        # 1. Прямой переход на Google
        browser.get("https://www.google.com/ncr")
        time.sleep(random.uniform(2, 4))

        # 2. Проверка CAPTCHA
        if "sorry" in browser.current_url:
            pytest.skip(f"CAPTCHA обнаружена при входе для '{query}'")

        # 3. Принятие куки (новые селекторы 2024)
        try:
            cookie_buttons = [
                "//button[.//span[contains(., 'Accept all')]]",
                "//button[contains(., 'Accept all')]",
                "//button[contains(., 'I agree')]"
            ]

            for xpath in cookie_buttons:
                try:
                    cookie_btn = WebDriverWait(browser, 3).until(
                        EC.element_to_be_clickable((By.XPATH, xpath)))
                    cookie_btn.click()
                    print("  Куки приняты")
                    time.sleep(1)
                    break
                except:
                    continue
        except:
            print("  Окно с куками не появилось")

        # 4. Поиск поля ввода (актуальные селекторы 2024)
        search_selectors = [
            "textarea[type='search']",
            "textarea[name='q']",
            "input[type='text']",
            "[name='q']"
        ]

        search_box = None
        for selector in search_selectors:
            try:
                search_box = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                break
            except:
                continue

        if not search_box:
            browser.save_screenshot("search_box_not_found.png")
            pytest.fail("Не удалось найти поле поиска")

        # 5. Человекообразный ввод с улучшенной эмуляцией
        print("  Имитируем человеческий ввод...")
        search_box.clear()
        human_type(search_box, query)

        # 6. Отправка запроса с ожиданием
        time.sleep(random.uniform(0.8, 1.5))
        search_box.send_keys(Keys.RETURN)
        print("  Запрос отправлен")
        time.sleep(random.uniform(2, 4))

        # 7. Проверка CAPTCHA после поиска
        if "sorry" in browser.current_url:
            pytest.skip(f"CAPTCHA после поиска для '{query}'")

        # 8. Поиск результатов (актуальные селекторы 2024)
        result_selectors = [
            "div.g",  # Классические результаты
            "div[data-snf]",  # Новый формат
            "div[role='main'] div:has(> h3)",  # Альтернативный формат
            "h3"  # Просто заголовки
        ]

        results = None
        for selector in result_selectors:
            try:
                elements = WebDriverWait(browser, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
                if len(elements) > 3:
                    results = elements
                    break
            except:
                continue

        if not results:
            browser.save_screenshot(f"no_results_{query}.png")
            pytest.fail(f"Не найдены результаты для '{query}'")

        print(f"  Найдено результатов: {len(results)}")
        assert len(results) > 5, f"Мало результатов ({len(results)}) для '{query}'"

    except Exception as e:
        browser.save_screenshot(f"error_{query}.png")
        print(f"  Ошибка: {str(e)}")
        raise