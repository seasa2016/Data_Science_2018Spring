import requests
from bs4 import BeautifulSoup as bf

url = "https://www.ptt.cc/bbs/beauty/index.html"
base = "https://www.ptt.cc"

r = requests.get(url)
#print(r.text)

soup = bf(r.text.encode('utf-8'),"html.parser")

#follow up is the data that need to be save
for line in soup.find_all(class_="r-ent"):
    temp = line.find_all(class_=["date","title"])

    print(temp)    

    print('date:{0}'.format(temp[1].text.strip().replace('/','')))
    print('title:{0}'.format(temp[0].text[1:-1]))
    print('url:{0}'.format(base+temp[0].find("a")['href']))
    break
