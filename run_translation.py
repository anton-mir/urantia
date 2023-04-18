#!/usr/bin/python3

"""
License Copyright: Unlicense.org.
License License: CC0 1.0 Universal (CC0 1.0).
SPDX short identifier: Unlicense

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information about the license, please refer to http://unlicense.org/
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from langdetect import detect

import time
import re
import sys
import yaml
import os

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

PROMPT_DELAY_SEC = config["prompt_delay_sec"]
REPLY_DELAY_SEC = config["reply_delay_sec"]


def save_config():
    with open(f"config.yaml", "w") as f:
        yaml.dump(config, stream=f, default_flow_style=False, sort_keys=False)


def wait_time(time_to_wait):
    start_time = time.time()

    while time.time() - start_time < time_to_wait:
        time.sleep(1)
        print(
            "Waiting... Time to recheck: %3d"
            % (time_to_wait - (time.time() - start_time)),
            end="\r",
            flush=True,
        )
    print(
        " " * 40,
        end="\r",
        flush=True,
    )


def wait_chat_reply():
    start_time = time.time()
    gray_response_field_len_prev = 0

    while time.time() - start_time < REPLY_DELAY_SEC:
        time.sleep(1)
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


def click_green_button():
    try:
        green_buttons = browser.find_elements(
            By.XPATH, '//button[@class="btn relative btn-primary m-auto"]'
        )
        if (
            len(green_buttons) == 1
            and green_buttons[0].text == "Regenerate response"
        ):
            green_buttons[0].send_keys("browser" + Keys.ENTER)
            wait_time(PROMPT_DELAY_SEC)
            wait_chat_reply()
        elif len(green_buttons) == 0:
          print("Nothing green")
        else:
          print(f"Found {len(green_buttons)} green something, refresh the page")
          browser.refresh()
          wait_time(PROMPT_DELAY_SEC)
    except NoSuchElementException:
        print(f"No green button, {time.asctime()}")


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


def limit_reached_loop():
    print(f"Limit reached (or error) at {time.asctime()}")

    while find_red_field() is not None or find_input_field() is None:
        click_green_button()
        wait_time(PROMPT_DELAY_SEC)

    browser.refresh()
    wait_time(PROMPT_DELAY_SEC)


def send_chat_request_and_wait_answer(request, exit_on_failure=False):
    while True:
        wait_time(PROMPT_DELAY_SEC)
        input_field = find_input_field()

        if input_field is not None:
            input_field.send_keys(request)
            input_field.send_keys(Keys.RETURN)

            wait_time(PROMPT_DELAY_SEC)

            if find_red_field() is not None:
                limit_reached_loop()
            else:
                print(f"Request sent at {time.asctime()}")
                wait_chat_reply()
                responses = browser.find_elements(By.XPATH, "//p[1]")
                answer = responses[-2].text.strip()
                if len(answer) > config["min_answer_length"]:
                    return answer
                else:
                    print("Wrong answer, too small, try again")

        elif exit_on_failure:
            exit()
        else:
            print("No input field found, try search for green button")
            click_green_button()
            browser.refresh()


def new_document_start(document_name=None):
    current_chat_url = ""
    new_chat_id = ""
    document_number = document_name.split(" ")[1]

    while len(current_chat_url) != 65 and len(new_chat_id) != 36:
        browser.get(f"https://chat.openai.com/chat?model=gpt-4")
        request_chat_name = f"Repeat after me: {document_name}"
        print(send_chat_request_and_wait_answer(request_chat_name))
        wait_chat_reply()

        chats_list_side = browser.find_elements(
            By.XPATH,
            "//a[starts-with(@class,'flex py-3 px-3 items-center gap-3 relative rounded-md')]",
        )
        ActionChains(browser).move_to_element(
            chats_list_side[1]
        ).click().perform()
        time.sleep(5)
        chats_list_side = browser.find_elements(
            By.XPATH,
            "//a[starts-with(@class,'flex py-3 px-3 items-center gap-3 relative rounded-md')]",
        )
        ActionChains(browser).move_to_element(
            chats_list_side[0]
        ).click().perform()

        current_chat_url = str(browser.current_url)
        new_chat_id = current_chat_url.split("/")[-1]

    print(f"New Paper number is {document_number}")
    print(f"The current url of new chat is: {current_chat_url}")
    print(f"New chat ID is {new_chat_id}")

    if new_chat_id != "chat?model=gpt-4":
        config["chat_id"] = new_chat_id
        config["paper_number"] = document_number
    save_config()
    print(send_chat_request_and_wait_answer(config["initial_request_text"]))


def process_line():
    global line_index
    global lines_from_file

    line = lines_from_file[line_index]
    print("=" * 40)
    print(f"Chat url is {str(browser.current_url)}")
    print(f"Start new cycle with the line {line_index+1}:")
    print(line.strip())
    if (
        line == ""
        or re.search("^[A-Z -]*$", line)  # "THE NATURE OF GOD"
        or re.search("^[0-9]*\. ", line)  # "1. THE INFINITY OF GOD"
        or re.search("^-.*$", line)  # "-------"
    ):
        print(f"Line {line_index+1} skip")
        line_index += 1
        return  # Skip such lines

    elif re.search(r"^Paper [0-9]*", line, flags=0):
        print("New document translation start")
        new_document_start(document_name=line.strip())
        line_index += 1
        return  # Skip "The Urantia Book" line

    same_answer_counter = 0
    wrong_reply_counter = 0
    while True:
        # Send current line request
        answer = send_chat_request_and_wait_answer(line.strip())

        if detect(answer) != "uk":
            if wrong_reply_counter == 1 and re.search(
                r"^[0-9]*\:[0-9]*\.[0-9]* \([0-9]*\.[0-9]*\) \[.*\]",
                answer,
                flags=0,
            ):
                print("This was last line of the document with authorship")
                print(f"Line {line_index+1}/{len(lines_from_file)}:\n{answer}")
                break
            elif wrong_reply_counter == 1 and len(answer) < 50:
                print("This might be short string... Let it go.")
                print(f"Line {line_index+1}/{len(lines_from_file)}:\n{answer}")
                break
            elif wrong_reply_counter == 1:
                print("Asked to use Ukrainian only once.")
                break
            print(
                f"Wrong answer language: {answer}\n"
                "Ask chat again to translate to Ukrainian"
            )
            wrong_reply_counter += 1
            # Send initial request
            send_chat_request_and_wait_answer(config["initial_request_text"])
        elif answer == config["last_answer"]:
            if same_answer_counter < 2:
                print("ERROR: Got same answer as previous, will try next line ")
                same_answer_counter += 1
            elif same_answer_counter == 2:
                line_index += 1
                line = lines_from_file[line_index]
            else:
                print("ERROR: Got same answer constantly! ")
                exit()
        else:
            print(f"Line {line_index+1}/{len(lines_from_file)}:\n{answer}")
            break

    with open(
        os.path.join(
            "./TheUrantiaBook/Ukrainian",
            f"Книга_Урантії_{config['paper_number']}.txt",
        ),
        "a",
    ) as f:
        f.write(answer)
        f.write("\n")

    line_index += 1
    config["last_answer"] = answer


if __name__ == "__main__":
    lines_from_file = open(
        os.path.join(
            "./TheUrantiaBook/English",
            f"The_Urantia_Book_{config['paper_number']}.txt",
        ),
        "r",
    ).readlines()
    # Get start line number as first command line argument
    if len(sys.argv) > 1:
        start_line_index = int(sys.argv[1]) - 1
        print(f"Command line argument: start from line {start_line_index+1}")
    elif config["start_from_line"] - 1 >= 0 and config[
        "start_from_line"
    ] - 1 < len(lines_from_file):
        start_line_index = config["start_from_line"] - 1
        print(
            "Config with previously processed line: start "
            f"from line {start_line_index+1}, Paper {config['paper_number']}"
        )
    else:
        start_line_index = 0
        print(
            f"Start by default from line {start_line_index+1}, Paper {config['paper_number']}"
        )

    options = ChromeOptions()
    options.debugger_address = f"127.0.0.1:{config['debug_port']}"
    options.add_argument("start-maximized")

    browser = webdriver.Chrome(
        service=Service(config["driver_path"]), options=options
    )
    browser.get(f"https://chat.openai.com/chat/{config['chat_id']}")

    wait_time(PROMPT_DELAY_SEC)

    assert start_line_index >= 0 and start_line_index < len(
        lines_from_file
    ), "Wrong start line"

    if len(sys.argv) == 3 and sys.argv[2] == "True":
        print("Start with request to translate to Ukrainian")
        send_chat_request_and_wait_answer(
            config["initial_request_text"], exit_on_failure=True
        )

    print(
        f"{time.asctime()}: Starting translation. {len(lines_from_file)} lines in file."
        f" Start from {start_line_index+1} line."
    )

    line_index = start_line_index

    while True:
        while line_index < (len(lines_from_file)):
            browser.get(f"https://chat.openai.com/chat/{config['chat_id']}")
            process_line()
            # Save last processed line to config
            config["start_from_line"] = line_index + 1
            save_config()

        print(f"End Paper {config['paper_number']}!")
        config["paper_number"] = int(config["paper_number"]) + 1
        line_index = 0
        config["start_from_line"] = line_index + 1
        save_config()

        lines_from_file = open(
            os.path.join(
                "./TheUrantiaBook/English",
                f"The_Urantia_Book_{config['paper_number']}.txt",
            ),
            "r",
        ).readlines()

    browser.quit()
