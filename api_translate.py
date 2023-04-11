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

import openai
import time

openai.api_key = "{KEY}"

file_u = open('Doc1_eng.txt', 'r')
Lines = file_u.readlines()
outputs = []

count = 0

response = openai.Completion.create(
      model="{model}",
      prompt=f"Translate the lines that I will send to you in the following "
      "requests from English to Ukrainian as professional translator. "
      "Do not remove the paragraph number from the beginning of the line.",
      temperature=0.3,
      max_tokens=2013,
    )

if response["choices"][0]["finish_reason"] == "error":
        print(f"Error: {response['choices'][0]['text']}")
else:
    print(response.choices[0].text, "\n")

for line in Lines:
    if line == "":
          continue
    count += 1
    print("Line {}: \n{}".format(count, line.strip()))

    response = openai.Completion.create(
      model="{model}",
      prompt=f"{line.strip()}",
      temperature=0.3,
      max_tokens=1700,
    )
    if response["choices"][0]["finish_reason"] == "error":
            print(f"Error: {response['choices'][0]['text']}")
            break
    else:
        output = response.choices[0].text
        print("Translation:")
        print(output, "\n")
        outputs.append(output)

with open(f"translated_doc1_{time.time()}.txt", "w") as output_file:
        output_file.write("\n".join(outputs))
