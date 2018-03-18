import requests
from bs4 import BeautifulSoup as bf
import time
import sys
import bisect
from operator import itemgetter


start_time = time.time()

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
            #time.sleep(0.01)
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
                try:
                    url_check = base+line.find(class_="title").find("a")['href']
                    r = requests.get(url_check)
                    time.sleep(0.01)
                    content = bf(r.text.encode('utf-8'),"html.parser").text
                    """
                    if(content.find('作者') == -1 or content.find('發信站: 批踢踢實業坊(ptt.cc), 來自: ') == -1 ):       
                        continue
                    """
                    if(content.find('※ 發信站:') == -1 ):       
                        continue
                    
                except TypeError:
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
        start_date = int(sys.argv[2])
        end_date = int(sys.argv[3])
        
        accu=[{},{}]
        data=[]
        f = open('all_articles.txt','r')
        for line in f:

            ll = line.find(',')
            rr = line.rfind(',')
            temp = [int(line[:ll]),line[ll+1:rr],line[rr+1:-1]]

            if( not ( (temp[0] <= end_date) and (temp[0] >= start_date))):
                continue    
            data.append(temp)
        like=0
        boo=0
        for line in data:
            time.sleep(0.01)
            try:
                r = requests.get(line[2])
            except requests.exceptions.MissingSchema:
                print(line)
                print('test')
                sys.exit(0)
            soup = bf(r.text.encode('utf-8'),"html.parser")
            content = soup.text
            content = soup.text.split("\n")
            #print(content)
            
            cc=0
            index = -1
            for __ in content:
                if('※ 發信站: ' in __):
                    index = cc
                cc += 1
            for line in content[index:]:
                line = line.split()
                if( len(line) <= 1 ):
                    continue
                elif( line[0] == '推' ):
                    category = 0
                    like+=1
                elif( line[0] == '噓' ):
                    category = 1
                    boo+=1
                elif( line[0] == '→' ):
                    continue
                else:
                    continue
                
                try:
                    accu[ category ][ line[1] ]+=1
                except KeyError:
                    accu[ category ][ line[1] ]=1
                except IndexError:
                    print("????????????")
                    print(content)
                    sys.exit(0)
                
                #break            
            #break

        #print(accu)
        f = open('push[{0}-{1}].txt'.format(start_date,end_date),'w')
        
        temp = []
        temp.append( [( _ , -accu[0][_] ) for _ in accu[0]] )
        temp.append( [( _ , -accu[1][_] ) for _ in accu[1]] )
        
        temp[0] = sorted(temp[0], key=itemgetter(1,0))
        temp[1] = sorted(temp[1], key=itemgetter(1,0))
       
         
        f.write('all like: {}\n'.format(like))
        f.write('all boo: {}\n'.format(boo))

        for _ in temp[0]:
            f.write(str(_)+"\n")
        for _ in temp[1]:
            f.write(str(_)+"\n")

        for _ in range(min(len(temp[0]),10)):
            f.write('like #{0}: {1} {2}\n'.format(_,temp[0][_][0],-temp[0][_][1]))
        
        for _ in range(min(len(temp[1]),10)):
            f.write('boo #{0}: {1} {2}\n'.format(_,temp[1][_][0],-temp[1][_][1]))
            
    elif(sys.argv[1] == 'popular'):
        start_date = int(sys.argv[2])
        end_date = int(sys.argv[3])
        
        data=[]
        f = open('./ans/all_popular.txt','r')
        for line in f:

            ll = line.find(',')
            rr = line.rfind(',')
            temp = [int(line[:ll]),line[ll+1:rr],line[rr+1:-1]]

            if( not ( (temp[0] <= end_date) and (temp[0] >= start_date))):
                continue    
            data.append(temp)
        
        like=0
        boo=0


        f = open('popular[{0}-{1}].txt'.format(start_date,end_date),'w')
        f.write('number of popular articles: {0}\n'.format(len(data)))
        

        for line in data:
            time.sleep(0.05)
            try:
                r = requests.get(line[2])
            except requests.exceptions.MissingSchema:
                print(line)
                sys.exit(0)
        
            soup = bf(r.text.encode('utf-8'),"html.parser")
            content = soup.find_all('a')

            for mess in content:
                ur = mess.get('href')
                
                if(ur[:4]=='http'):
                    if( ur[-4:]=='.jpg' or ur[-5:]=='.jpeg' or ur[-4:]=='.png' or ur[-4:]=='.gif'):
                            f.write(ur+'\n')
                    


    elif('keyword' in sys.argv[1]):
        
        ll = sys.argv[1].find('(')
        rr = sys.argv[1].rfind(')')
            
        keyword = sys.argv[1][ll+1:rr]
        print(keyword)
        start_date = int(sys.argv[2])
        end_date = int(sys.argv[3])
        
        data=[]
        f = open('all_articles.txt','r')
        for line in f:

            ll = line.find(',')
            rr = line.rfind(',')
            temp = [int(line[:ll]),line[ll+1:rr],line[rr+1:-1]]

            if( not ( (temp[0] <= end_date) and (temp[0] >= start_date))):
                continue    
            data.append(temp)
        
        like=0
        boo=0


        f = open('keyword[{0}-{1}].txt'.format(start_date,end_date),'w')      

        for line in data:
            time.sleep(0.05)
            try:
                r = requests.get(line[2])
            except requests.exceptions.MissingSchema:
                print(line)
                sys.exit(0)
        
            soup = bf(r.text.encode('utf-8'),"html.parser")
            content = soup.text
            content = soup.text.split("\n")

            checker = False

            for mess in content:
                if('作者' in mess):
                    checker = True
                if(checker == False):
                    continue
                if('※ 發信站:' in mess):
                    break
                
                if(keyword in mess):
                    for ur_temp in soup.find_all('a'):
                        ur = ur_temp.get('href')
                        
                        if(ur[:4]=='http'):
                            if( ur[-4:]=='.jpg' or ur[-5:]=='.jpeg' or ur[-4:]=='.png' or ur[-4:]=='.gif'):
                                    f.write(ur+'\n')
                            

end_time = time.time()
print('Time : '+ str(end_time-start_time) + ' sec.')




