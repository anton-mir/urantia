from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

from langdetect import detect

import time
import re
import sys
import yaml
import os

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

FILENAME_PREFIX = config["filename_prefix"]
LINES = open(
    os.path.join("./TheUrantiaBook/English", f"{FILENAME_PREFIX}_eng.txt"),
    "r",
).readlines()
PROMPT_DELAY_SEC = config["prompt_delay_sec"]
REPLY_DELAY_SEC = config["reply_delay_sec"]
INITIAL_REQUEST_TEXT = config["initial_request_text"]


def wait_chat_reply():
    start_time = time.time()
    gray_response_field_len_prev = 0

    while time.time() - start_time < REPLY_DELAY_SEC:
        time.sleep(2)
        print(
            "Waiting %3d..." % (REPLY_DELAY_SEC - (time.time() - start_time)),
            end="\r",
            flush=True,
        )
        try:
            response_requests_gray = browser.find_elements(By.TAG_NAME, "p")
        except NoSuchElementException:
            print(f"No answer messages, {time.asctime()}")
        # End when chat response complete
        if gray_response_field_len_prev == len(response_requests_gray[-2].text):
            break
        gray_response_field_len_prev = len(response_requests_gray[-2].text)

    print(
        "               ",
        end="\r",
        flush=True,
    )


def find_red_field():
    response_request_red = None
    try:
        response_request_red = browser.find_element(
            By.CSS_SELECTOR, "div[class*='bg-red']"
        )
    except NoSuchElementException:
        print(f"No red limit message, {time.asctime()}")
    return response_request_red


def find_input_field():
    input_field = None
    try:
        input_field = browser.find_element(By.XPATH, "//textarea[1]")
    except NoSuchElementException:
        print(f"No input field, {time.asctime()}")
    return input_field


def send_chat_request(request, exit_on_fail=False):
    input_field = find_input_field()

    if input_field is not None:
        input_field.send_keys(request)
        input_field.send_keys(Keys.RETURN)
        print(f"Request sent, {time.asctime()}")
        time.sleep(PROMPT_DELAY_SEC)
    elif exit_on_fail:
        exit()
    else:
        browser.refresh()
        time.sleep(PROMPT_DELAY_SEC)


def limit_reached_loop():
    print(f"\nLimit reached or error at {time.asctime()}")

    while find_red_field() is not None or find_input_field() is None:
        print("Waiting...", end="\r", flush=True)
        time.sleep(5)

    browser.refresh()
    time.sleep(PROMPT_DELAY_SEC)


def send_request_for_translation_and_wait_answer(
    request_for_translation, exit_on_failure=False
):
    while True:
        browser.refresh()
        time.sleep(PROMPT_DELAY_SEC)
        send_chat_request(
            request=request_for_translation, exit_on_fail=exit_on_failure
        )

        if find_red_field() is not None:
            limit_reached_loop()
        else:
            print(f"Request sent, translation started at {time.asctime()}")
            wait_chat_reply()
            responses = browser.find_elements(By.XPATH, "//p[1]")
            return responses[-2].text.strip()


def process_line():
    global line_index
    line = LINES[line_index - 1]
    if (
        line == ""
        or re.search(r"^Paper [0-9]*", line, flags=0)  # "Paper 2"
        or re.search(r"^[A-Z ’]*$", line, flags=0)  # "THE NATURE OF GOD"
        or re.search(r"^[0-9]*\. ", line, flags=0)  # "1. THE INFINITY OF GOD"
        or re.search(r"^-.*$", line, flags=0)  # "-------"
    ):
        print(f"Line {line_index} skip")
        return  # Skip such lines

    elif re.search(r"The Urantia Book", line, flags=0):  # "The Urantia Book"
        print("New document translation start")
        send_chat_request(request=INITIAL_REQUEST_TEXT, exit_on_fail=True)
        response_request_red = find_red_field()
        if response_request_red is not None:
            print("Limit reached at the start of the Document")
            limit_reached_loop()
            send_chat_request(request=INITIAL_REQUEST_TEXT, exit_on_fail=True)
        return  # Skip "The Urantia Book" line

    same_answer_counter = 0
    while True:
        # Send current line request
        answer = send_request_for_translation_and_wait_answer(line.strip())

        if detect(answer) != "uk":
            print(
                f"Wrong answer language: {answer}\n"
                "Ask chat again to translate to Ukrainian"
            )
            # Send initial request
            send_request_for_translation_and_wait_answer(INITIAL_REQUEST_TEXT)
        elif answer == config["last_answer"]:
            if same_answer_counter < 2:
                print("ERROR: Got same answer as previous, will try next line ")
                same_answer_counter += 1
            elif same_answer_counter == 2:
                line += 1
                line = LINES[line_index - 1]
            else:
                print("ERROR: Got same answer constantly! ")
                exit()
        else:
            print(f"Line {line_index}/{len(LINES)}:\n{answer}")
            break

    with open(
        os.path.join(
            "./TheUrantiaBook/Ukrainian", f"{FILENAME_PREFIX}_ukr.txt"
        ),
        "a",
    ) as f:
        f.write(answer)
        f.write("\n")

    line_index += 1
    config["last_answer"] = answer


if __name__ == "__main__":
    # Get start line number as first command line argument
    if len(sys.argv) > 1:
        start_line_index = int(sys.argv[1])
        print(f"Command line argument: start from line {start_line_index}")
    elif config["last_processed_line"] > 0 and config[
        "last_processed_line"
    ] < len(LINES):
        start_line_index = config["last_processed_line"] + 1
        print(
            "Config with previously processed line: start "
            f"from line {start_line_index}"
        )
    else:
        start_line_index = 1
        print(f"Start by default from line {start_line_index}")

    options = ChromeOptions()
    options.debugger_address = "127.0.0.1:" + "8888"
    options.add_argument("start-maximized")

    browser = webdriver.Chrome(
        service=Service(config["driver_path"]), options=options
    )
    browser.get(f"https://chat.openai.com/chat/{config['chat_id']}")

    time.sleep(PROMPT_DELAY_SEC)

    assert start_line_index >= 1 and start_line_index <= len(
        LINES
    ), "Wrong start line"

    if len(sys.argv) == 3 and sys.argv[2] == "True":
        print("Start with request to translate to Ukrainian")
        send_request_for_translation_and_wait_answer(
            INITIAL_REQUEST_TEXT, exit_on_failure=True
        )

    print(
        f"{time.asctime()}: Starting translation. {len(LINES)} lines in file."
        f" Start from {start_line_index} line."
    )

    line_index = start_line_index

    while line_index < (len(LINES) + 1):
        process_line()
        # Save last processed line to config
        config["last_processed_line"] = line_index
        with open(f"config.yaml", "w") as f:
            yaml.dump(
                config, stream=f, default_flow_style=False, sort_keys=False
            )
    print("End!")
    browser.quit()
