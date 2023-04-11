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

import os
import re

LINES = open(
    os.path.join(
        "./TheUrantiaBook/English", f"UF-ENG-001-1955-20.5.txt"
    ),
    "r",
).readlines()

line_index = 0
line = LINES[line_index]


while line_index < len(LINES):
    # Search start
    while not re.search(r"^Paper [0-9]*", line, flags=0):
        line_index += 1
        line = LINES[line_index]
    # Read name
    document_number = line.split(" ")[1].strip()
    doc_name = f"The_Urantia_Book_{document_number}.txt"
    # Till end
    while not re.search(r"^-.*$", line, flags=0):
        with open(
            os.path.join(
                "./TheUrantiaBook/", doc_name
                ),
                "a",
            ) as f:
                f.write(line)
        line_index += 1
        if line_index < len(LINES):
          line = LINES[line_index]
        else:
          break

print("Done")
