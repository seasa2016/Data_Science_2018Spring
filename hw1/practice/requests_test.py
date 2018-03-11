import requests
url = ""
r = requests.get(url)
print(r.text)