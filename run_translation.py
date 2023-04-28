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
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ActionChains

from langdetect import detect

import pyautogui
import datetime
import time
import re
import sys
import yaml
import os
import random
import inspect
import subprocess

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

PROMPT_DELAY_SEC = config["prompt_delay_sec"]
REPLY_DELAY_SEC = config["reply_delay_sec"]
browser_global = None
red_text_global = None

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

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


def findThisProcess(process_name):
  ps = subprocess.Popen("ps -A | grep "+process_name, shell=True, stdout=subprocess.PIPE)
  output = str(ps.stdout.read())
  ps.stdout.close()
  ps.wait()

  return output

def isThisRunning(process_name):
  output = findThisProcess(process_name)

  if re.search(process_name, output) is None:
    return False
  else:
    return True

def wait_chat_reply():
    global browser_global
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
            response_requests_gray = browser_global.find_elements(
                By.TAG_NAME, "p"
            )
        except NoSuchElementException:
            print(f"{lineno()}: No answer messages, {time.asctime()}")
        # End when chat response complete
        if gray_response_field_len_prev == len(response_requests_gray[-2].text):
            break
        gray_response_field_len_prev = len(response_requests_gray[-2].text)

    print(
        "               ",
        end="\r",
        flush=True,
    )


def move_to(offset_x, offset_y):
    global browser_global
    x = offset_x
    y = offset_y
    while x > 0 or y > 0:
        x = x - 1 if x > 0 else 0
        y = y - 1 if y > 0 else 0
        ActionChains(browser_global).move_by_offset(
            1 if x > 0 else 0, 1 if y > 0 else 0
        ).perform()
        time.sleep(0.1)


def click_human(time_click=1):
    global browser_global
    try:
        human_checkbox = browser_global.find_element(
            By.XPATH, '//div[@id="challenge-stage"]'
        )
        print(f"{lineno()}: Click checkbox and wait {time_click} sec")
        ActionChains(browser_global).move_to_element(human_checkbox)
        for i in range(3, random.randint(5, 10)):
            move_to(random.randint(10, 25), random.randint(5, 15))
            time.sleep(random.randint(1, 4))
        ActionChains(browser_global).click().perform()
        wait_time(time_click)
    except NoSuchElementException:
        print(f"{lineno()}: NoSuchElementException, {time.asctime()}")
        wait_time(time_click)
    except ElementNotInteractableException:
        print(f"{lineno()}: ElementNotInteractableException, {time.asctime()}")
        wait_time(time_click)


def click_recorded():
    global browser_global
    wait_time(3)
    recording_lines_from_file = open(
        "mouse_m.txt",
        "r",
    ).readlines()
    target_x = 835
    target_y = 635
    click = False
    for line in recording_lines_from_file:
        mouseX, mouseY, m_delay = line.split()
        mouseX = int(mouseX)
        mouseY = int(mouseY)
        time.sleep(float(m_delay))
        pyautogui.moveTo(mouseX, mouseY)
        x_approve = mouseX >= target_x - 5 and mouseX <= target_x + 5
        y_approve = mouseY >= target_y - 5 and mouseY <= target_y + 5
        print("AUTOGUI: ", mouseX, mouseY, x_approve, y_approve, click)
        if x_approve and y_approve:
            if click == False:
                pyautogui.click()
                print("CLICK!")
                click = True
        elif not x_approve and not y_approve:
            click = False
    wait_time(5)

def click_green_button():
    global browser_global
    try:
        green_buttons = browser_global.find_elements(
            By.XPATH, '//button[@class="btn relative btn-primary m-auto"]'
        )
        if (
            len(green_buttons) == 1
            and green_buttons[0].text == "Regenerate response"
        ):
            green_buttons[0].send_keys("browser" + Keys.ENTER)
            wait_time(PROMPT_DELAY_SEC)
            wait_chat_reply()
            return True
        elif len(green_buttons) == 0:
            print(f"{lineno()}: Nothing green, refresh")
            browser_global.refresh()
            browser_global.get(
                f"https://chat.openai.com/chat/{config['chat_id']}"
            )
            wait_time(PROMPT_DELAY_SEC)
            return False
        else:
            print(
                f"{lineno()}: Found {len(green_buttons)} green something, refresh the page"
            )
            browser_global.refresh()
            wait_time(PROMPT_DELAY_SEC)
            return False
    except NoSuchElementException:
        print(f"{lineno()}: No green button, {time.asctime()}")
        return False


def find_check_red_field():
    global browser_global
    global red_text_global
    red_text_global = None
    try:
        red_text_global = browser_global.find_element(
            By.CSS_SELECTOR, "div[class*='bg-red']"
        )
        print(
            f"{lineno()}: Red limit message found: {red_text_global.text}, {time.asctime()}"
        )
        if re.search(
          r"current usage cap",
          red_text_global.text,
          flags=0,
          ):
          print(f"{lineno()}: Usage cap loop start")
          wait_for_allowance(red_text_global.text)
        else:
          print(f"{lineno()}: Some other red message appeared, refresh")
          browser_global.refresh()
    except NoSuchElementException:
        print(f"{lineno()}: No red limit message, {time.asctime()}")

def find_input_field():
    global browser_global
    input_field = None
    try:
        input_field = browser_global.find_element(By.XPATH, "//textarea[1]")
        print(f"{lineno()}: Input field found, {time.asctime()}")
    except NoSuchElementException:
        print(f"{lineno()}: No input field, {time.asctime()}")
    return input_field


def timeConversion(s):
    if "PM" in s:
        s = s.replace("PM", " ")
        t = s.split(":")
        if t[0] != "12":
            t[0] = str(int(t[0]) + 12)
            s = (":").join(t)
        return s
    else:
        s = s.replace("AM", " ")
        t = s.split(":")
        if t[0] == "12":
            t[0] = "00"
            s = (":").join(t)
        return s


def wait_for_allowance(red_text):
    print(f"{lineno()}: Wait for allowance started")
    date_time_now = datetime.datetime.now().strftime("%I:%M%p")
    date_time_now = timeConversion(date_time_now)
    date_time_now_hour = int(date_time_now.split(":")[0])
    date_time_now_minute = int(date_time_now.split(":")[1])

    wait_until = (red_text.split()[-4] + red_text.split()[-3]).replace(".", "")
    wait_until = timeConversion(wait_until)
    wait_until_hour = int(wait_until.split(":")[0])
    wait_until_minute = int(wait_until.split(":")[1])

    wait_needed_sec = 30 # Add 30 sec to wait time
    if wait_until_hour >= date_time_now_hour:
        wait_needed_sec = (
            wait_needed_sec + (wait_until_hour - date_time_now_hour) * 60 * 60
        )
    else:
        wait_needed_sec = (
            wait_needed_sec
            + ((wait_until_hour + 24) - date_time_now_hour) * 60 * 60
        )

    if wait_until_minute >= date_time_now_minute:
        wait_needed_sec = (
            wait_needed_sec + (wait_until_minute - date_time_now_minute) * 60
        )
    else:
        wait_needed_sec = (
            wait_needed_sec
            + ((wait_until_minute + 60) - date_time_now_minute) * 60
        )
    print(
        f"{lineno()}: Wait until red message end {wait_needed_sec} sec "
        f"({wait_needed_sec/60} min or {wait_needed_sec/(60*60)} hours)"
    )
    print("Open the window now then!")
    wait_time(wait_needed_sec)


def limit_reached_loop():
    global browser_global
    global red_text_global

    print(f"{lineno()}: Limit reached (or error) at {time.asctime()}")
    cycle_counter = 0
    while True:
        print(f"{lineno()}: Limit reached loop cycle {cycle_counter}, {time.asctime()}")
        click_green_button()
        wait_time(PROMPT_DELAY_SEC)
        cycle_counter += 1
        find_check_red_field()

        # Have NO RED message
        if find_input_field() is not None:
          # Have INPUT field
          print(f"{lineno()}: Exit limit reached loop")
          break
        else:
          # Have NO INPUT field
          print(f"{lineno()}: Run mouse replay because of the prompt")
          if isThisRunning('mouse_replay') == False:
            print("Run mouse replay now")
            exit()
          else:
            print("Mouse replay is active, will not run it")

    browser_global.refresh()
    wait_time(PROMPT_DELAY_SEC)


def send_chat_request_and_wait_answer(request, exit_on_failure=False):
    global browser_global
    global red_text_global

    while True:
        wait_time(PROMPT_DELAY_SEC)
        input_field = find_input_field()

        if input_field is not None:
            input_field.send_keys(request)
            input_field.send_keys(Keys.RETURN)
            print(f"{lineno()}: This request sent: {request}")

            wait_time(PROMPT_DELAY_SEC)
            find_check_red_field()
            # ----
            if find_input_field() is None:
              print(f"{lineno()}: Run mouse replay because of the prompt")
              if isThisRunning('mouse_replay') == False:
                print("Run mouse replay now")
                exit()
              else:
                print("Mouse replay is active, will not run it")
                continue

            print(f"{lineno()}: Request sent at {time.asctime()}")
            wait_chat_reply()
            responses = browser_global.find_elements(By.XPATH, "//p[1]")
            answer = responses[-2].text.strip()
            if len(answer) > config["min_answer_length"]:
                return answer
            else:
                print(f"{lineno()}: Wrong answer, too small, try again")
            # if red_text_global is not None:
            #     limit_reached_loop()
            # else:
            #     print(f"{lineno()}: Request sent at {time.asctime()}")
            #     wait_chat_reply()
            #     responses = browser_global.find_elements(By.XPATH, "//p[1]")
            #     answer = responses[-2].text.strip()
            #     if len(answer) > config["min_answer_length"]:
            #         return answer
            #     else:
            #         print(f"{lineno()}: Wrong answer, too small, try again")

        elif exit_on_failure:
            exit()
        else:
            print(f"{lineno()}: No input field found, try search for green button")
            result = click_green_button()
            print(f"{lineno()}: Result of search is ",result)
            if result is False:
              print(f"{lineno()}: Run mouse replay because of the prompt")
              if isThisRunning('mouse_replay') == False:
                print("Run mouse replay now")
                exit()
              else:
                print("Mouse replay is active, will not run it")
                continue

def new_document_start(document_name=None):
    global browser_global
    current_chat_url = ""
    new_chat_id = ""
    document_number = document_name.split(" ")[1]

    while len(current_chat_url) != 65 and len(new_chat_id) != 36:
        browser_global.get(f"https://chat.openai.com/chat?model=gpt-4")
        request_chat_name = f"Repeat after me: {document_name}"
        print(send_chat_request_and_wait_answer(request_chat_name))
        wait_chat_reply()

        chats_list_side = browser_global.find_elements(
            By.XPATH,
            "//a[starts-with(@class,'flex py-3 px-3 items-center gap-3 relative rounded-md')]",
        )
        ActionChains(browser_global).move_to_element(
            chats_list_side[1]
        ).click().perform()
        time.sleep(5)
        chats_list_side = browser_global.find_elements(
            By.XPATH,
            "//a[starts-with(@class,'flex py-3 px-3 items-center gap-3 relative rounded-md')]",
        )
        ActionChains(browser_global).move_to_element(
            chats_list_side[0]
        ).click().perform()

        current_chat_url = str(browser_global.current_url)
        new_chat_id = current_chat_url.split("/")[-1]

    print(f"{lineno()}: New Paper number is {document_number}")
    print(f"{lineno()}: The current url of new chat is: {current_chat_url}")
    print(f"{lineno()}: New chat ID is {new_chat_id}")

    if new_chat_id != "chat?model=gpt-4":
        config["chat_id"] = new_chat_id
        config["paper_number"] = document_number
    save_config()
    print(send_chat_request_and_wait_answer(config["initial_request_text"]))


def process_line():
    global browser_global
    global line_index
    global lines_from_file

    line = lines_from_file[line_index]
    print("=" * 40)
    print(f"{lineno()}: Chat url is {str(browser_global.current_url)}")
    print(f"{lineno()}: Start new cycle with the line {line_index+1}:")
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
        print(f"{lineno()}: New document translation start")
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
                print(f"{lineno()}: This was last line of the document with authorship")
                print(f"Line {line_index+1}/{len(lines_from_file)}:\n{answer}")
                break
            elif wrong_reply_counter == 1 and len(answer) < 50:
                print(f"{lineno()}: This might be short string... Let it go.")
                print(f"Line {line_index+1}/{len(lines_from_file)}:\n{answer}")
                break
            elif wrong_reply_counter == 1:
                print(f"{lineno()}: Asked to use Ukrainian only once.")
                break
            print(
                f"{lineno()}: Wrong answer language: {answer}\n"
                "Ask chat again to translate to Ukrainian"
            )
            wrong_reply_counter += 1
            # Send initial request
            send_chat_request_and_wait_answer(config["initial_request_text"])
        elif answer == config["last_answer"]:
            if same_answer_counter < 2:
                print(f"{lineno()}: ERROR: Got same answer as previous, will try next line ")
                same_answer_counter += 1
            elif same_answer_counter == 2:
                line_index += 1
                line = lines_from_file[line_index]
            else:
                print(f"{lineno()}: ERROR: Got same answer constantly! ")
                exit()
        else:
            print(f"{lineno()}: Line {line_index+1}/{len(lines_from_file)}:\n{answer}")
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
        print(f"{lineno()}: Command line argument: start from line {start_line_index+1}")
    elif config["start_from_line"] - 1 >= 0 and config[
        "start_from_line"
    ] - 1 < len(lines_from_file):
        start_line_index = config["start_from_line"] - 1
        print(
            f"{lineno()}: Config with previously processed line: start "
            f"from line {start_line_index+1}, Paper {config['paper_number']}"
        )
    else:
        start_line_index = 0
        print(
            f"{lineno()}: Start by default from line {start_line_index+1}, Paper {config['paper_number']}"
        )

    options = ChromeOptions()
    options.debugger_address = f"127.0.0.1:{config['debug_port']}"
    options.add_argument("start-maximized")

    browser_global = webdriver.Chrome(
        service=Service(config["driver_path"]), options=options
    )
    browser_global.get(f"https://chat.openai.com/chat/{config['chat_id']}")

    wait_time(PROMPT_DELAY_SEC)

    assert start_line_index >= 0 and start_line_index < len(
        lines_from_file
    ), "Wrong start line"

    if len(sys.argv) == 3 and sys.argv[2] == "True":
        print(f"{lineno()}: Start with request to translate to Ukrainian")
        send_chat_request_and_wait_answer(
            config["initial_request_text"], exit_on_failure=True
        )

    print(
        f"{lineno()}: {time.asctime()}: Starting translation. {len(lines_from_file)} lines in file."
        f" Start from {start_line_index+1} line."
    )

    line_index = start_line_index

    while True:
        while line_index < (len(lines_from_file)):
            browser_global.get(
                f"https://chat.openai.com/chat/{config['chat_id']}"
            )
            process_line()
            # Save last processed line to config
            config["start_from_line"] = line_index + 1
            save_config()

        print(f"{lineno()}: End Paper {config['paper_number']}!")
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

    browser_global.quit()
