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
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

PROMPT_DELAY_SEC = 5

def wait_chat_reply():
    start_time = time.time()
    gray_response_field_len_prev = 0

    while True:
        time.sleep(1)
        print(
            "Waiting %3d..." % ((time.time() - start_time)),
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

options = ChromeOptions()
options.debugger_address = "127.0.0.1:" + "8888"
options.add_argument("start-maximized")
driver_path = "/home/user/chromedriver/"

browser = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"), options=options
)
browser.get(f"https://chat.openai.com/chat?model=gpt-4")

time.sleep(PROMPT_DELAY_SEC)

input_field = browser.find_element(By.XPATH, "//textarea[1]")
input_field.send_keys("Name this conversation with random fruit name and number")
input_field.send_keys(Keys.RETURN)

wait_chat_reply()

input_fields = browser.find_elements(
    By.XPATH,
    "//a[starts-with(@class,'flex py-3 px-3 items-center gap-3 relative rounded-md')]",
)

ActionChains(browser).move_to_element(input_fields[0]).click().perform()

get_url = browser.current_url
print("The current url is:" + str(get_url))

browser.quit()
