# Urantia Ukraine

Ukrainian Translation of The Urantia Book

Scripts to translate The Urantia Book with Chat GPT

1 Create ChatGPT4 session with Plus account and save the link to it
2 Insert link to script as LINK_TO_CHAT_THREAD
3 Prepare Doc1_eng.txt with lines to be translated
4 Install selenium:
$ pip3 install selenium
5 Check your version of the Chrome
6 Download the Selenium driver for the specific Chrome version https://chromedriver.chromium.org/downloads
7 Put it to ~/chromedriver and to /usr/bin/
8 Add proper path to driver_path variable in script
9 Run:
$ echo 'export PATH=$PATH:/home/{user}/chromedriver' >> ~/.bash_profile
$ source ~/.bash_profile
10 Run chrome with:
$ google-chrome --remote-debugging-port=8888 --user-data-dir=/home/{user}/chromedriver/
11 In other terminal run:
$ python3 run_translation.py