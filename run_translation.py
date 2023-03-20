"""
Run translation line-by-line from Doc1_eng.txt to Doc1_ukr.txt
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

import time
import re
from datetime import timedelta

FILENAME_PREFIX = "Doc2"
FILE_U = open(f"{FILENAME_PREFIX}_eng.txt", "r")
LINES = FILE_U.readlines()
PROMPT_DELAY_SEC = 12
REPLY_DELAY_SEC = 180
MAX_REQUESTS_PER_HOUR = 25
REQUEST_EXCESS_TIME_SEC = 3 * 60 * 60 + 60  # 3 hours + 1 minute
DRIVER_PATH = "/usr/bin/chromedriver"
LINK_TO_CHAT_THREAD = "https://chat.openai.com/chat/{ID}"

start_time = time.time()
response_request_limit = 0


def process_line(line, request_counter):
    global start_time
    if (
        line == ""
        or re.search(r'^Paper [0-9]*', line, flags = 0) # "Paper 2"
        or re.search(r"^[A-Z ]*$", line, flags=0) # "THE NATURE OF GOD"
        or re.search(r"^[0-9]*\. ", line, flags=0) # "1. THE INFINITY OF GOD"
    ):
        return # Skip such lines

    try:
        input_field = browser.find_element(By.XPATH, "//textarea[1]")
        input_field.send_keys(f"{line.strip()}")
        input_field.send_keys(Keys.RETURN)
        time.sleep(PROMPT_DELAY_SEC)
    except NoSuchElementException:
        pass

    try:
        response_request_limit = browser.find_elements(
            By.LINK_TEXT, "Learn more"
        )
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
                response_request_limit = browser.find_elements(
                    By.LINK_TEXT, "Learn more"
                )
            except NoSuchElementException:
                pass

            time_to_wake = REQUEST_EXCESS_TIME_SEC - (time.time() - start_time)

        time_to_wake = 0
        start_time = time.time()
        request_counter = 0
        print("Starting again\n")

    waiting_started = time.time()
    while time.time() - waiting_started < REPLY_DELAY_SEC:
        time.sleep(1)
        print(
            "Waiting for chat answer "
            f"{REPLY_DELAY_SEC - (time.time() - waiting_started)}",
            end="\r",
            flush=True,
        )

    responses = browser.find_elements(By.XPATH, "//p[1]")
    print("Request ", request_counter, ":\n", responses[-2].text)

    with open(f"{FILENAME_PREFIX}_ukr.txt", "a") as f:
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
