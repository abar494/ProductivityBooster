import base64

with open("topImage.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    print(encoded_string)

#write to output.txt
    
with open("output.txt", "w") as text_file:
    text_file.write(encoded_string.decode('utf-8'))
#read json file and update
    
import json

request = {}

request["requests"] = [{}]
request["requests"][0]["image"] = {}
request["requests"][0]["image"]["content"] = encoded_string.decode('utf-8')
request["requests"][0]["features"] = [{}]
request["requests"][0]["features"][0]["type"] = "TEXT_DETECTION"
request["requests"][0]["features"][0]["maxResults"] = 1
request["requests"][0]["features"][0]["model"] = "builtin/latest"

with open('request.json', 'w') as f:
    json.dump(request, f, indent=4)