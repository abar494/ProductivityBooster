# import subprocess

# curlRequest = "curl -X POST -H Authorization: Bearer $(gcloud auth application-default print-access-token) -H" +\
# "Content-Type: application/json; charset=utf-8" +\
# "https://vision.googleapis.com/v1/images:annotate" +\
# "-d @request.json -o response.json"
import re

# Regex pattern splits on substrings "; " and ", "

# checker = subprocess.check_output(hey, shell=True).decode("utf-8")


# print("time to analyse response")

import pytesseract

heya = pytesseract.image_to_string('tester.png', timeout=3)

heya = heya.strip()
# .split(" ", "\n")

heya = re.split(' |\n', heya)

# print(heya)
# print(heya)
#check if heya has a word that contains www
a = True
for word in heya:
    if "www" in word:
        print("AWESOME")
        print(word)
        a = False
        # break
if a:
    print("No www in this word")