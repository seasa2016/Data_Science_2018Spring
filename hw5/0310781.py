import numpy as np
import pandas as pd

train_data=pd.read_csv('./data-science-hw-5nctuxnthu/train.csv')
test_data=pd.read_csv('./data-science-hw-5nctuxnthu/test.csv')
train_data = train_data[train_data['rating'] != 99].reset_index()

train_data['user_id']=train_data[['user_id']].astype('int')
train_data['item_id']=train_data[['item_id']].astype('int')

test_data['user_id']=test_data[['user_id']].astype('int')
test_data['item_id']=test_data[['item_id']].astype('int')

train_data['rating'] = train_data['rating'].apply(lambda x: 0 if(x==99) else x)

data,label = train_data[['user_id','item_id']],train_data[['rating']]

from sklearn.model_selection import train_test_split

data_train, data_val,label_train,label_val = train_test_split(data,label,test_size = 0.2,random_state = 0)
arr_train = pd.concat([data_train,label_train], axis=1, ignore_index=False)
arr_val = pd.concat([data_val,label_val], axis=1, ignore_index=False)

class MF():
    
    def __init__(self, R_train,R_test,num_users,num_items):
        self.samples_train = R_train
        self.samples_test = R_test
        self.num_users, self.num_items = num_users,num_items
        # Create a list of training samples
        print('prepare data')
        print('fin')
    def train_set(self,K,alpha,beta,iterations):
        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations
        
        
        # Initialize user and item latent feature matrice
        self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
        self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))
        
        # Initialize the biases
        self.b_u = np.zeros(self.num_users, dtype=np.float64)
        self.b_i = np.zeros(self.num_items, dtype=np.float64)
        #self.b = np.mean(self.R_train[np.where(self.R_train != 0)])
        self.b = 0
    
    def train(self):
        # Perform stochastic gradient descent for number of iterations
        training_process = []
        testing_process = []
        for i in range(self.iterations):
            print(i)
            np.random.shuffle(self.samples_train)
            self.sgd()
            
            mse_train,mse_test = self.mse()
            
            training_process.append((i, mse_train))
            testing_process.append((i, mse_test))
            
            if (i+1) % 2 == 0:
                print("Iteration: %d\terror_train = %.4f\terror_test = %.4f " % (i+1,mse_train,mse_test))
            
            if (i+1) % 15 == 0:
                self.alpha /= 2
        print(self.full_matrix())
        return training_process

    def mse(self):
        """
        A function to compute the total mean square error
        """        
        predicted = self.full_matrix()
        
        index = 5000
        error_train = 0
        for x, y ,r in self.samples_train:
            error_train += pow(r - predicted[x, y], 2)
            
        error_test = 0
        for x, y ,r in self.samples_test:
            error_test += pow(r - predicted[x, y], 2)
            
        
        return np.sqrt(error_train / len(self.samples_train)),np.sqrt(error_test / len(self.samples_test))

    def sgd(self):
        """
        Perform stochastic graident descent
        """
        for i, j, r in self.samples_train:
            # Computer prediction and error
            prediction = self.get_rating(i, j)
            e = (r - prediction)
            
            """
            print("------------------------")
            print(r,prediction)
            print(i,self.P[i, :],self.b_u[i])
            print(j,self.Q[j, :],self.b_i[j])
            print("------------------------")
            """
            
            # Update biases
            self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])
            self.b_i[j] += self.alpha * (e - self.beta * self.b_i[j])
            # Update user and item latent feature matrices
            self.P[i, :] += self.alpha * (e * self.Q[j, :] - self.beta * self.P[i,:])
            self.Q[j, :] += self.alpha * (e * self.P[i, :] - self.beta * self.Q[j,:])
            
            
            
    def get_rating(self, i, j):
        """
        Get the predicted rating of user i and item j
        """
        #prediction = self.P[i, :].dot(self.Q[j, :].T)
        prediction = self.b + self.b_u[i] + self.b_i[j] + self.P[i, :].dot(self.Q[j, :].T)
        return prediction
    
    def full_matrix(self):
        """
        Computer the full matrix using the resultant biases, P and Q
        """
        return self.b + self.b_u[:,np.newaxis] + self.b_i[np.newaxis:,] + self.P.dot(self.Q.T)

samples_train = [
    ( int(arr_train.iloc[i]['user_id']-1),int(arr_train.iloc[i]['item_id']-1), arr_train.iloc[i]['rating'])
    for i in range(arr_train.shape[0])]

samples_test = [
    (int(arr_val.iloc[i]['user_id']-1), int(arr_val.iloc[i]['item_id']-1), arr_val.iloc[i]['rating'])
    for i in range(arr_val.shape[0])]

mf = MF(samples_train,samples_test,10000,100)
K = 50
alpha = 0.01
beta = 0.3
iterations = 20

mf.train_set(K, alpha, beta, iterations)
mf.train()

aans = mf.full_matrix()
f_out = open('ans.out','w')

f_out.write("user_id-item_id,rating\n")
for i in range(test_data.shape[0]):
    print(i)
    f_out.write("{0}-{1},{2}\n".format(test_data.iloc[i]['user_id'],test_data.iloc[i]['item_id'],aans[ test_data.iloc[i]['user_id']-1 ][ test_data.iloc[i]['item_id']-1 ]))
    
f_out.close()
