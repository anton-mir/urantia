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
input_field.send_keys("Translate all following requests in this conversation from the \
English to Ukrainian language as professional translator keeping the numbers at \
the beginning. Translate to the Ukrainian language only. Don't use any other language \
in this conversation ever.")
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
