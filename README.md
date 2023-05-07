# Книга Урантії для України / Urantia Book for Ukraine

![alt text](https://avatars.githubusercontent.com/u/8962479?s=400&u=c10ade6e3ff453fe8404edfd097a0a1c19d5a075&v=4)

# Український переклад Книги Урантії

Цей репозиторій містить скріпти, опубліковані за ліцензією [Unlicense](http://unlicense.org/), що можуть використовуватися для перекладу Книги Урантії українською мовою з оригінального англійського тексту через Chat GPT v.4.0.

Оригінальний текст Книги Урантії опубліковано Фондом Урантія на https://www.urantia.org, див. розділ [Download](https://www.urantia.org/urantia-book/download-text-urantia-book)

Оригінальний англійський текст Книги Урантії знаходиться у відкритому доступі (Public Domain) з 2006 року.

Український переклад Книги Урантії, опублікований у цьому репозиторії в
теці [TheUrantiaBook/Ukrainian](https://github.com/anton-mir/urantia/tree/main/TheUrantiaBook/Ukrainian) слід вважати текстом у суспільному надбанні
за ліцензією [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.uk).

Будь-хто може долучитися до роботи з корекції і покращення перекладу в цьому
репозиторії або на сайті https://urantia-ua.atlassian.net/wiki/spaces/ubukr.
Для цього будь ласка контактуйте будь-яким зручним вам способом. Контактну інформацію можна занйти за цими посиланнями:

* https://github.com/anton-mir
* https://www.urantia.org.ua
* https://urantia-ua.atlassian.net

# Ukrainian Translation of The Urantia Book

This repository contains [Unlicense](http://unlicense.org/) Copyrighted scripts that are used to hold the to translate The Urantia Book to the Ukrainian Language from the English original text published by The Urantia Foundation with Chat GPT v.4.0

For the original The Urantia Book text please refer to https://www.urantia.org,
section [Download](https://www.urantia.org/urantia-book/download-text-urantia-book)

Original English text of The Urantia Book is in Public Domain since 2006.

The Ukrainian translation of TheUrantia Book published in this repository under
the [TheUrantiaBook/Ukrainian](https://github.com/anton-mir/urantia/tree/main/TheUrantiaBook/Ukrainian) folder should be considered as Public Domain text
under the [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

# How to use the translation script / Як налаштувати переклад

0. Get OpenAI Plus account

1. Create here https://chat.openai.com/chat Model GPT-4 session with and save the direct link to it

2. Insert link to config_example.yaml, and rename it to "config.yaml"

3. Install selenium and maybe other dependencies:

```
$ pip3 install selenium
```

4. Check your version of the Chrome and download the Selenium driver for your Chrome version https://chromedriver.chromium.org/downloads

5. Put the Selenium driver to ~/chromedriver (might be not needed) and to /usr/bin/

6. Run:
```
$ echo 'export PATH=$PATH:/home/{user}/chromedriver' >> ~/.bash_profile (might be not needed)
$ source ~/.bash_profile
```
7. Run chrome with:
```
$ google-chrome --remote-debugging-port=[port_number, see config, may be 8888] --user-data-dir=/home/{user}/chromedriver/
```
8. In the newly opened Chrome window go to https://chat.openai.com/chat and
log in to your Plus account

9. In the new terminal window run:
```
$ python3 run_translation.py [optional: line_to_start_with_number] [optional: start_with_initial_request_text_true_or_false]
```
