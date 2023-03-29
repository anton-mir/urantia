from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

PROMPT_DELAY_SEC = 5
CHAT_ID = ""


options = ChromeOptions()
options.debugger_address = "127.0.0.1:" + "8888"
options.add_argument("start-maximized")
driver_path = "/home/user/chromedriver/"

browser = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"), options=options
)
browser.get(f"https://chat.openai.com/chat/{CHAT_ID}")

time.sleep(PROMPT_DELAY_SEC)

green_buttons = None
try:
    green_buttons = browser.find_elements(
        By.XPATH, '//button[@class="btn relative btn-primary m-auto"]'
    )
    if (
        len(green_buttons) == 1
        and green_buttons[0].text == "Regenerate response"
    ):
        green_buttons[0].send_keys("browser" + Keys.ENTER)
except NoSuchElementException:
    print(f"No button, {time.asctime()}")


browser.quit()
