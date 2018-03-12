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
    info = soup.find_all(class_="btn-group btn-group-paging")[0].find_all(class_="btn wide")
    
    url = base + info[1]['href']
    #print(url)

    #end loop if in the first page
    if( len(info) == 3 and '下頁' in info[1].text):
        break

    key=1
    #second we parse the data
    for line in soup.find_all(class_="r-ent"):
        
        temp = []
        sasa=line.text.split("\t")
        for _ in sasa: 
            temp.extend(_.split("\n"))
        sasa = temp
        temp = list(filter(lambda x: x != '',sasa)) 
        print(temp)
        
        
        if( ('(本文已被刪除)' in temp[-3]) or ('[公告]' in temp[-3][0:4])):
            continue
        
        if(len(temp)==5):
            temp.pop(1)


        data.append({  'date': int(temp[-2].replace('/','')),
                        'title':temp[-3],
                        'url':base+line.find(class_="title").find("a")['href'],  
                        'type':temp[0]  
                    })

        """
        temp = line.find_all(class_=["title","date"])

        title = temp[0].text[1:-1].strip()
        
        if( ('(本文已被刪除)' in title) or ('[公告]' in title[0:4])):
            continue
        
        
        data.append({  'date': int(temp[1].text.strip().replace('/','')),
                        'title':temp[0].text[1:-1],
                        'url':base+temp[0].find("a")['href']    
                    })
        
        print('date:{0}'.format(temp[1].text.strip().replace('/','')))
        print('title:{0}'.format(temp[0].text[1:-1]))
        print('url:{0}'.format(base+temp[0].find("a")['href']))
        """
        #print('-----')
        #break
    break

for _ in data:
    print(_)
#print(data[0])
"""
f = open('all_articles.txt','w')
for line in data:
    f.write('{0},{1},{2}\n'.format(line['date'],line['title'],line['url']))
"""