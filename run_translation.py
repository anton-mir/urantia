"""
$ cat ~/.bash_selenium
export PATH=$PATH:/home/user/chromedriver

Run chrome with:
. ~/.bash_selenium
google-chrome --remote-debugging-port=8888 --user-data-dir=/home/user/chromedriver/
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

import time
from datetime import timedelta

FILE_U = open("Doc1_eng.txt", "r")
LINES = FILE_U.readlines()
PROMPT_DELAY_SEC = 12
REPLY_DELAY_SEC = 100
MAX_REQUESTS_PER_HOUR = 25
REQUEST_EXCESS_TIME_SEC = 3 * 60 * 60 + 60  # 3 hours + 1 minute
DRIVER_PATH = "/usr/bin/chromedriver"
LINK_TO_CHAT_THREAD = (
    "https://chat.openai.com/chat/[ID]]"
)

start_time = time.time()
response_request_limit = 0

def process_line(line, request_counter):
    global start_time
    if line == "":
        return

    try:
        input_field = browser.find_element(By.XPATH, "//textarea[1]")
        input_field.send_keys(f"{line.strip()}")
        input_field.send_keys(Keys.RETURN)
        time.sleep(PROMPT_DELAY_SEC)
    except NoSuchElementException:
        pass

    try:
      response_request_limit = browser.find_elements(By.LINK_TEXT, "Learn more")
    except NoSuchElementException:
      pass

    if (
        len(response_request_limit) >= 1
        or request_counter >= MAX_REQUESTS_PER_HOUR
    ):
        time_to_wake = REQUEST_EXCESS_TIME_SEC - (time.time() - start_time)

        print("\nLimit reached!")
        while time_to_wake > 0 or len(response_request_limit) >= 1:
            print(
                "Sleeping. Time to wake up left: "
                f"{str(timedelta(seconds=time_to_wake))}",
                end="\r",
                flush=True,
            )

            time.sleep(5)

            try:
                input_field = browser.find_element(By.XPATH, "//textarea[1]")
                input_field.send_keys(f"{line.strip()}")
                input_field.send_keys(Keys.RETURN)
                time.sleep(PROMPT_DELAY_SEC)
            except NoSuchElementException:
                pass

            try:
              response_request_limit = browser.find_elements(By.LINK_TEXT, "Learn more")
            except NoSuchElementException:
              pass

            time_to_wake = REQUEST_EXCESS_TIME_SEC - (time.time() - start_time)

        time_to_wake = 0
        start_time = time.time()
        request_counter = 0
        print("Starting again\n")

    responses = browser.find_elements(By.XPATH, "//p[1]")
    print("Request ", request_counter, " : ", responses[-2].text)

    with open("Doc1_ukr.txt", "a") as f:
        f.write(responses[-2].text)
        f.write("\n")


if __name__ == "__main__":

    options = ChromeOptions()
    options.debugger_address = "127.0.0.1:" + "8888"
    options.add_argument("start-maximized")

    browser = webdriver.Chrome(service=Service(DRIVER_PATH), options=options)
    browser.get(LINK_TO_CHAT_THREAD)

    time.sleep(PROMPT_DELAY_SEC)

    request_counter = 0

    for line in LINES:
        process_line(line, request_counter)
        request_counter += 1

    browser.quit()
