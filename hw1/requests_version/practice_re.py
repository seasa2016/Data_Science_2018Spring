import requests
from bs4 import BeautifulSoup as bf
import time
import sys

if(len(sys.argv) == 1):
    sys.exit(0)
else:
    if(sys.argv[1]=='crawl'):
        url = "https://www.ptt.cc/bbs/beauty/index.html"
        base = "https://www.ptt.cc"
        data=[]
        key = [False,False,False]
        while(1):
            #use url to fetch new page
            r = requests.get(url)
            time.sleep(0.01)
            soup = bf(r.text.encode('utf-8'),"html.parser")
            #follow up is the data that need to be save
            
            #first we get the next page url
            info = soup.find_all(class_="btn-group btn-group-paging")[0].find_all(class_="btn wide")
            
            url = base + info[1]['href']
            #print(url)

            #end loop if in the first page
            if( len(info) == 3 and '下頁' in info[1].text):
                break

            #second we parse the data
            word = soup.find_all(class_="r-ent")
            word.reverse()
            for line in word:
                temp = []
                sasa=line.text.split("\t")
                for _ in sasa: 
                    temp.extend(_.split("\n"))
                sasa = temp
                temp = list(filter(lambda x: x != '',sasa)) 
                
                
                if( ('(本文已被刪除)' in temp[-3]) or ('[公告]' in temp[-3][0:4])):
                    continue
                url_check = base+line.find(class_="title").find("a")['href']
                r = requests.get(url_check)
                time.sleep(0.1)
                content = bf(r.text.encode('utf-8'),"html.parser").text

                if(content.find('作者') == -1 or content.find('發信站: 批踢踢實業坊(ptt.cc), 來自: ') == -1 ):       
                    continue

                if(len(temp)==5):
                    temp.pop(1)
                elif(len(temp)==3):
                    temp.insert(0,'0')
                    
                #print(temp)

                temp[-2] = int(temp[-2].replace('/',''))
                if(key[0] == False):
                    if(temp[-2] != 1231):
                        continue
                    else:
                        key[0] = True
                else:
                    if(temp[-2] == 101):
                        key[1] = True
                    if(key[1]==True):
                        if(temp[-2] != 101):
                            key[2] = True
                            break

                try:
                    data.insert(0,{ 'date': temp[-2],
                                    'title':temp[-3],
                                    'url':base+line.find(class_="title").find("a")['href'],  
                                    'type':temp[0]  
                                })
                except TypeError:
                    pass
            if(key[2]):
                break

        """
        for _ in data:
            print(_)
        """
        #print(data[0])

        f = open('all_articles.txt','w')
        for line in data:
            f.write('{0},{1},{2}\n'.format(line['date'],line['title'],line['url']))

        f = open('all_popular.txt','w')
        for line in data:
            if(line['type']=='爆'):
                f.write('{0},{1},{2}\n'.format(line['date'],line['title'],line['url']))
    elif(sys.argv[1] == 'push'):

    elif(sys.argv[1] == 'popular'):
        
    elif(sys.argv[1] == 'keyword'):
        