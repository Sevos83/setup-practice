import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_search_results(query):
    driver = webdriver.Chrome()
    try:
        print(f"\nТестируем запрос: '{query}'")
        driver.get("https://duckduckgo.com/")

        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )

        # Постепенный ввод
        for ch in query:
            search_box.send_keys(ch)
            time.sleep(random.uniform(0.1, 0.3))

        search_box.send_keys(Keys.RETURN)

        # Ждем результаты
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )

        results = driver.find_elements(By.CSS_SELECTOR, "article")
        print(f"Найдено результатов: {len(results)}")
        assert len(results) > 5, f"Для '{query}' найдено только {len(results)} результатов"

    finally:
        driver.quit()


if __name__ == "__main__":
    pytest.main(["-v"])