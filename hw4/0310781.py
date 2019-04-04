#first we can do some preprocess on training data
def ddfs(route,now,check,l,ss):    
    l.append(now)
    check[now] = 0

    if(now not in route):
        check[now] = 1

        for i in range(len(l)):
            for j in range(i+1,len(l)):
                try:
                    ss[ l[i] ].add(l[j])
                except KeyError:
                    ss[ l[i] ] = set()
                    ss[ l[i] ].add(l[j])

        return l.copy()
    
    else:
        nex = False

        arr=[]
        for i in route[now]:
            if(check[i]):    
                arr.append(ddfs(route,i,check,l,ss))
                l.remove(l[-1])
                
                check[i] = 1
                nex = True

        arr = sorted(arr,key=lambda x: len(x),reverse= True)

        #return longest
        if(nex):
            if(len(arr)):
                return arr[0].copy()
            else:
                return []
        else:
            return l.copy()


f = open('./data-science-hw-3-nctuxnthu/train.csv','r')
f.readline()

path={}

for data in f:
    data = data.strip().split(',')

    data = [int(_) for _ in data]
    if(data[-1]==0):
        temp = data[1]
        data[1] = data[2]
        data[2] = temp

    try:
        path[data[0]][data[1]].append(data[2])
    except KeyError as e:
        if(e.args[0] == data[0]):
            path[data[0]] = {}
            path[data[0]][data[1]] = [data[2]]

        elif(e.args[0] == data[1]):
            path[data[0]][data[1]] = [data[2]]

f.close()

f = open('./data-science-hw-3-nctuxnthu/new_train.csv','w')
f.write("User ID,Item1 ID,Item2 ID,Preference\n")


ans={}
count = 0
for i in range(1,61):
    print(i)
    ans[i]=[]
    
    ss={}
    
    for j in range(1,11):
        check=[1]*11
        l=[]
        ans[i].append(ddfs(path[i],j,check,l,ss))
    #remove the contradiction
    for a in range(1,11):
        for b in range(a+1,11):
            try:
                if( (b in ss[a]) and (a in ss[b]) ):
                    ss[a].remove(b)
                    ss[b].remove(a)
                    print(i,a,b)
            except KeyError:
                pass
    for _ in ss:
        for num in ss[_]:
            f.write("{0},{1},{2},{3}\n".format(i,_,num,1))

    ans[i] = sorted(ans[i],key= lambda x:len(x),reverse = True)
    print(ans[i][0])

#this version add up the one hot encoding for some feature
import pandas as pd
pd.options.mode.chained_assignment = None

user = pd.read_csv('./data-science-hw-3-nctuxnthu/users.csv')
item = pd.read_csv('./data-science-hw-3-nctuxnthu/items.csv')
train = pd.read_csv('./data-science-hw-3-nctuxnthu/new_train.csv')
test = pd.read_csv('./data-science-hw-3-nctuxnthu/test.csv')

re = pd.get_dummies(user['Region'])
user=pd.concat([user.drop('Region',axis=1),re],axis=1)

user['Education'] = user['Education'].apply(lambda x: user['Education'].mode()[0] if(x==0) else x  )
user['Gender'] = user['Gender'].apply(lambda x: user['Gender'].mode()[0] if(x==0) else x  )

test['rank']=range(1311)
train2 = train.copy()

train2['Preference'] = train2['Preference'].apply(lambda x : -x+1)
train2['temp'] = train2['Item1 ID']
train2['Item1 ID'] = train2['Item2 ID']
train2['Item2 ID'] = train2['temp']
train2 = train2[['User ID','Item1 ID','Item2 ID','Preference']]

train_out = pd.concat([train,train2],axis=0,ignore_index=True)
train_out.reset_index(inplace=True, drop=True)
train_out
#train_out = train

train_out = pd.merge(train_out,user,how='inner', on='User ID')
test_out = pd.merge(test,user,how='inner', on='User ID')

train_out = pd.merge(train_out,item,how='inner', left_on='Item1 ID',right_on='Item ID')
test_out = pd.merge(test_out,item,how='inner', left_on='Item1 ID',right_on='Item ID')

train_out = pd.merge(train_out,item,how='inner', left_on='Item2 ID',right_on='Item ID',suffixes=['1','2'])
test_out = pd.merge(test_out,item,how='inner', left_on='Item2 ID',right_on='Item ID',suffixes=['1','2'])

test_out=test_out.sort_values(by=['rank'])

test_out=test_out.reset_index()
train_out=train_out.reset_index()

data  = train_out[['Education','Age','Gender',1,2,3,4,'BodyType1','Transmission1','Engin Capacity1','Fuel Consumed1','BodyType2','Transmission2','Engin Capacity2','Fuel Consumed2']]
test_data  = test_out[['Education','Age','Gender',1,2,3,4,'BodyType1','Transmission1','Engin Capacity1','Fuel Consumed1','BodyType2','Transmission2','Engin Capacity2','Fuel Consumed2']]
label = train_out['Preference']

from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier

#7,0.18,0.6,100
xgbc = XGBClassifier(max_depth=7, learning_rate=0.180,colsample_bytree=0.6,n_estimators=100)

ss=0

x_train, x_test,y_train,y_test = train_test_split(data,label,test_size=0.2,random_state=i)
xgbc.fit(x_train,y_train)
ss += xgbc.score(x_test,y_test)

print('precision is {0}'.format(ss/20))

xgbc.fit(data,label)

ans = xgbc.predict(test_data)

test['Preference'] = ans
test['Preference'] = test['Preference'].astype(int)
test = test[['User ID','Item1 ID','Item2 ID','Preference']]
test.reset_index()

test.to_csv('submit1.csv', index= False,sep='-')

f = open('submit1.csv','r')
w = open('submit.csv','w')

w.write('User-Item1-Item2,Preference\n')

f.readline()
for line in f:
    line =line.strip().split('-')
    w.write('-'.join(line[:3]))
    w.write(',{0}\n'.format(line[3]))
