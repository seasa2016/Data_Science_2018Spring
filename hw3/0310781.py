from  sklearn.datasets import load_svmlight_file,dump_svmlight_file
import numpy as np
from numpy import linalg
import sys


def PCA(x):
    mu = np.mean(x,axis=0)

    nom = x-mu

    var = np.transpose(nom).dot(nom)
    
    var = (var + np.transpose(var)) / (len(x)*2)

    temp = np.linalg.eigh(var)
    
    normalize = temp[0] / np.sum(temp[0])
    mmax = max(normalize)

    temp =(temp[0],np.transpose(temp[1]))

    for i in range(len(normalize)):
        if((normalize[i] / mmax) > float(sys.argv[2])):
            fin = temp[0][i:]
            vector = temp[1][i:]
            break    
    return vector,mu

    


x,y = load_svmlight_file(sys.argv[1])
x = x.toarray()


"""
cut = int(x.shape[0]*0.8)

train_data,train_label = x[:cut],y[:cut]
val_data,val_label = x[cut:],y[cut:]

for i in range(train_data.shape[1]):
    train_data[:,i] = (train_data[:,i] - mean(train_data[:,i])) / variance(train_data[:,i]) 
"""

#train_data = np.array([[1,6,3],[2,4,1],[3,5,1]])
ans,mu = PCA(x)

"""
f = open(sys.argv[1].replace('.txt','_out.txt'),'w')
for line in ans:
    print(line)
"""
print(np.var((x-mu).dot(np.transpose(ans)),axis=0))

out_path = "./TestSample_HW3/"+sys.argv[1].replace('.txt','_out.txt')
dump_svmlight_file((x-mu).dot(np.transpose(ans)),y,out_path,zero_based=False)
