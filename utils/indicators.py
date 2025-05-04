# File: helpers/indicators.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def add_indicator_by_name(driver, indicator_name, timeout=10):
    """
    Opens the Quotex indicators panel and adds an indicator by its visible name.
    Args:
        driver: Selenium WebDriver instance
        indicator_name: Name of the indicator as it appears in the panel (e.g., "RSI", "MACD")
        timeout: Seconds to wait for elements to appear
    Returns:
        True if indicator was added, False otherwise
    """
    # 1. Click the chart ruler (indicators) button
    ruler_btn = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.icon-chart-ruler"))
    )
    ruler_btn.click()

    # 2. Wait for the indicators panel to appear
    panel = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "aside.sidepanel.app__sidepanel.sidepanel__bg-black.active"))
    )

    # 3. Find and click the indicator by name (case-insensitive)
    indicators = driver.find_elements(By.CSS_SELECTOR, "li.sidepanel__menu-item")
    for li in indicators:
        if li.text.strip().lower() == indicator_name.strip().lower():
            li.click()
            return True

    # If not found, close the panel and return False
    close_btn = driver.find_element(By.CSS_SELECTOR, "div.sidepanel__close")
    close_btn.click()
    return False
