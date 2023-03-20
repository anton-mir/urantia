# Urantia Ukraine

Ukrainian Translation of The Urantia Book

Scripts to translate The Urantia Book with Chat GPT

0. Get OpenAI Plus account

1. Create here https://chat.openai.com/chat Model GPT-4 session with and save the direct link to it

2. Insert link to script as _LINK_TO_CHAT_THREAD_

3. Prepare _Doc1_eng.txt_ with lines to be translated, one paragraph per line

4. Install selenium and maybe other dependencies:

```
$ pip3 install selenium
```

5. Check your version of the Chrome

6. Download the Selenium driver for the specific Chrome version https://chromedriver.chromium.org/downloads

7. Put it to ~/chromedriver and to /usr/bin/

8. Run:
```
$ echo 'export PATH=$PATH:/home/{user}/chromedriver' >> ~/.bash_profile
$ source ~/.bash_profile
```
9. Run chrome with:
```
$ google-chrome --remote-debugging-port=8888 --user-data-dir=/home/{user}/chromedriver/
```
10. In the newly opened Chrome window go to https://chat.openai.com/chat and log in

11. Update _FILENAME_PREFIX_ to match with input file name in the _run_translation.py_ script
like FILENAME_PREFIX = "Doc2" means "Doc2_eng.txt" as input

12. In the new terminal window run:
```
$ python3 run_translation.py
```
