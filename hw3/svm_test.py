from  sklearn.datasets import load_svmlight_file
import numpy as np
from numpy import linalg

def PCA(x):
    mu = np.mean(x,axis=0)

    var = np.zeros([len(x[0]),len(x[0])])
    
    print(x[0])
    print(var.shape)
    
    for i in range(len(x)):
        var += np.outer(x[i]-mu,x[i]-mu)
    var = var / len(x)

    var = (var + np.transpose(var))/2

    temp = np.linalg.eigh(var)
    print(temp[0])
    
    


x,y = load_svmlight_file('dataset2_sample.txt')

x = x.toarray()

cut = int(len(y)*0.8)

train_data,train_label = x[:cut],y[:cut]
test_data,test_label = x[cut:],y[cut:]

PCA(train_data)
