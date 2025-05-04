# utils/human_actions.py for OptiTradeBot

import random
import time
from selenium.webdriver.common.action_chains import ActionChains

def human_typing(element, text, delay_range=(0.05, 0.15)):
    """Type text into a Selenium element with human-like delays."""
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(*delay_range))

def human_click(driver, element, move_delay_range=(0.1, 0.3), click_delay_range=(0.05, 0.15)):
    """Move mouse to element and click with human-like pauses."""
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.pause(random.uniform(*move_delay_range))
    actions.click(element)
    actions.pause(random.uniform(*click_delay_range))
    actions.perform()

def human_wait(min_sec=0.2, max_sec=0.8):
    """Randomized wait to simulate human reaction time."""
    time.sleep(random.uniform(min_sec, max_sec))
