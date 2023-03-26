# Urantia Book for Ukraine

![alt text](https://avatars.githubusercontent.com/u/8962479?s=400&u=c10ade6e3ff453fe8404edfd097a0a1c19d5a075&v=4)

# Ukrainian Translation of The Urantia Book

Scripts to translate The Urantia Book with Chat GPT

0. Get OpenAI Plus account

1. Create here https://chat.openai.com/chat Model GPT-4 session with and save the direct link to it

2. Insert link to config.yaml, see an example file and rename it to "config.yaml"

3. Prepare for example _Doc1_eng.txt_ with lines to be translated, one paragraph per line, add prefix "Doc1" or other to config

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

11. In the new terminal window run:
```
$ python3 run_translation.py [line_to_start_number, number] [start_with_initial_request_text, just True or False]
```
