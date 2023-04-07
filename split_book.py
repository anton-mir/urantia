#!/usr/bin/python3

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
