from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
import time

PROMPT_DELAY_SEC = 12

options = ChromeOptions()
options.debugger_address = "127.0.0.1:" + "8888"
options.add_argument("start-maximized")
driver_path = "/home/amiroshn/chromedriver/"

browser = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"), options=options
)
browser.get("https://chat.openai.com/chat/[ID]")

time.sleep(PROMPT_DELAY_SEC)

input_field = browser.find_element(By.XPATH, "//textarea[1]")
input_field.send_keys("What is The Urantia Book?")
input_field.send_keys(Keys.RETURN)

time.sleep(PROMPT_DELAY_SEC)

responses = browser.find_elements(By.XPATH, "//p[1]")
print(responses[-2].text)

with open("responses.txt", "a") as f:
    f.write(responses[-2].text)
    f.write("\n")

browser.quit()
