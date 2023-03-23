from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
import time

PROMPT_DELAY_SEC = 12
CHAT_ID = "ID"

options = ChromeOptions()
options.debugger_address = "127.0.0.1:" + "8888"
options.add_argument("start-maximized")

browser = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"), options=options
)
browser.get(f"https://chat.openai.com/chat/{CHAT_ID}")

time.sleep(PROMPT_DELAY_SEC)

fields = []

try:
    response_requests_gray = browser.find_elements(
        By.CSS_SELECTOR, "div[class*='bg-gray']"
    )
except NoSuchElementException:
    print(f"No answer messages, {time.asctime()}")

print(response_requests_gray)
print()

browser.quit()
