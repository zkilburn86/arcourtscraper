from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def driver():
    from webdriver_manager.chrome import ChromeDriverManager

    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--headless")

    return webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
