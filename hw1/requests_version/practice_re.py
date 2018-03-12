import requests
from bs4 import BeautifulSoup as bf

url = "https://www.ptt.cc/bbs/beauty/index.html"
base = "https://www.ptt.cc"


data=[]

while(1):
    #use url to fetch new page
    r = requests.get(url)

    soup = bf(r.text.encode('utf-8'),"html.parser")
    #follow up is the data that need to be save
    
    #first we get the next page url
    
    
    #second we parse the data
    for line in soup.find_all(class_="r-ent"):
        temp = line.find_all(class_=["date","title"])

        title = temp[0].text[1:-1].strip()
        
        if( ('(本文已被刪除)' in title) or ('[公告]' in title[0:4])):
            continue
        
        data.append({  'date': int(temp[1].text.strip().replace('/','')),
                        'title':temp[0].text[1:-1],
                        'url':base+temp[0].find("a")['href']    
                    })
        """
        print('date:{0}'.format(temp[1].text.strip().replace('/','')))
        print('title:{0}'.format(temp[0].text[1:-1]))
        print('url:{0}'.format(base+temp[0].find("a")['href']))
        """
        #print('-----')
        #break
    break

for _ in data:
    print(_)