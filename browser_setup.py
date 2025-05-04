from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def launch_chrome_with_profile(user_data_dir, profile_directory="Default"):
    """
    Launch Chrome with the specified user profile.
    :param user_data_dir: Path to the Chrome user data directory (e.g., C:/Users/samir/AppData/Local/Google/Chrome/User Data)
    :param profile_directory: Profile folder name (e.g., "Default", "Profile 1")
    :return: Selenium WebDriver instance
    """
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")

    # You can add more options here if needed (e.g., headless mode)
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    return driver
