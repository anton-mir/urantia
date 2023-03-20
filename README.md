# Urantia Ukraine

Ukrainian Translation of The Urantia Book

Scripts to translate The Urantia Book with Chat GPT

1. Create ChatGPT4 session with Plus account and save the link to it

2. Insert link to script as _LINK_TO_CHAT_THREAD_

3. Prepare _Doc1_eng.txt_ with lines to be translated

4. Install selenium:

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
10. In other terminal run:
$ python3 run_translation.py