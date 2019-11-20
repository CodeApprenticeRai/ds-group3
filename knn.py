import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report

#import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('./test.csv')
df = df.drop(['s1', 's2', 's3', 's4', 'sharpe'],axis=1)

'''
normalized features
'''
scaler = StandardScaler()
scaler.fit(df.drop(['TARGET CLASS'],axis=1))
col  = df.drop(['TARGET CLASS'],axis=1).columns
scaler_feat = scaler.transform(df.drop(['TARGET CLASS'],axis=1))
df_feat = pd.DataFrame(scaler_feat,columns=col)
#print(df_feat.head())
#split features and label
X = df_feat
y = df['TARGET CLASS']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3)
'''
Use KNN
'''
#k = 3
'''
knn = KNeighborsClassifier(3)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
'''

#try more K values
error_rate = []
for i in range(1,40):
    knn = KNeighborsClassifier(i)
    knn.fit(X_train,y_train)
    y_pred_i = knn.predict(X_test)
    
    error_rate.append(np.mean(y_pred_i != y_test))

local_k = error_rate.index(min(error_rate))
print(local_k)

#plot results for different K
fig = plt.figure(figsize=(10,6))
plt.plot(range(1,40),error_rate,linestyle='--',marker='o',markersize=10)
plt.xlabel('K')
plt.ylabel('Error rate')
plt.show()

knn=KNeighborsClassifier(local_k)
knn.fit(X_train,y_train)
y_pred=knn.predict(X_test)

#back-test the data using QSTk and show result
print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))