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
