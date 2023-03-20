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
