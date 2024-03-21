import requests
from bs4 import BeautifulSoup

url = "http://example.com"
# url = "https://www.youtube.com/"
# url = "https://www.youtube.com/watch?v=PWgvGjAhvIw"

response = requests.get(url)

# print(response.text)

# parse the HTML
# soup = BeautifulSoup(response.text, "html.parser")

# object_methods = [method_name for method_name in dir(soup)
#                   if not callable(getattr(soup, method_name))]

# print(object_methods)


# print(soup.text)
# print(soup.body.get_text().strip())

# print(soup.body.get_text().strip())

# res = json.loads(zlib.decompress(response.content))

# print(type(soup))

# hey = json.dumps(soup.text)

# #write hey to json file
# with open('hey.json', 'w') as f:
#     f.write(hey)

# print(hey)