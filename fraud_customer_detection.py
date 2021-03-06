# -*- coding: utf-8 -*-
"""Fraud_customer_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19v4xRwFIOzzZcV-ghjRrE6tkpyOhuxCD
"""

# uploading two datasets

from google.colab import files
a=files.upload()
b=files.upload()



# import all required modules

import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np
import seaborn as sns

df1=pd.read_csv(io.BytesIO(a["Customer_DF (1).csv"]))
df2=pd.read_csv(io.BytesIO(b["cust_transaction_details (1)(1).csv"]))

# merge two datasets
# in df3 dataframe

df3=pd.merge(df2,df1,on="customerEmail")

"""***
**DATA ANALYSIS**
***
"""

df3.columns

df3.head()

df3.tail()

df3.shape

df3.info()

df3.describe()

"""***
**DATA PREPARATION and VISUALIZATION**
***
"""

# checking null values 
# if any in 
# dataframe

df3.isnull().sum()

# removing non 
# essential columns

nonessential_columns=["customerEmail","transactionId","orderId","paymentMethodId","paymentMethodProvider","customerPhone","customerDevice","customerIPAddress","customerBillingAddress","Unnamed: 0_y","Unnamed: 0_x"]

for i in nonessential_columns:
  df3=df3.drop(columns=[i],axis=1)

df3.head()

# converting str values
# in dataframe 
# to int format

df3["paymentMethodType"].unique()

df3["paymentMethodType"]=df3["paymentMethodType"].apply(lambda x:0 if x =="card" else x )
df3["paymentMethodType"]=df3["paymentMethodType"].apply(lambda x:1 if x =="bitcoin" else x )
df3["paymentMethodType"]=df3["paymentMethodType"].apply(lambda x:2 if x =="apple pay" else x )
df3["paymentMethodType"]=df3["paymentMethodType"].apply(lambda x:3 if x =="paypal" else x )

df3["orderState"].unique()

df3["orderState"]=df3["orderState"].apply(lambda x:0 if x=="pending" else x)
df3["orderState"]=df3["orderState"].apply(lambda x:1 if x=="fulfilled" else x)
df3["orderState"]=df3["orderState"].apply(lambda x:2 if x=="failed" else x)

df3["paymentMethodType"].unique()

# also converting 
# Fraud columns 
# with int values

df3["Fraud"]=df3["Fraud"].astype(int)

# new dataframe

df3.head()
a=df3



max(df3["transactionAmount"])

len(df3[df3["transactionAmount"]>100])

plt.plot(df3["transactionAmount"])

max(df3["transactionAmount"].iloc[300:534])

df3[400:410]

# remove row no 404

df3=df3.drop([404],axis=0)

m=max(df3["transactionAmount"])
m

df3["transactionAmount"]=df3["transactionAmount"].apply(lambda x:x/m)

plt.plot(df3["transactionAmount"])

df3.head()

a=max(df3["No_Transactions"])
a

b=max(df3["No_Payments"])
b

c=max(df3["No_Orders"])
c

df3["No_Transactions"]=df3["No_Transactions"].apply(lambda x:x/a)
df3["No_Payments"]=df3["No_Payments"].apply(lambda x:x/b)
df3["No_Orders"]=df3["No_Orders"].apply(lambda x:x/c)

df3.head()

sns.pairplot(df3)

cor=df3.corr()
sns.heatmap(cor,cmap="coolwarm")
cor

"""Here we see that the columns of dataframe i.e. No_Transactions ,transactionFailed ,paymentMethodType ,paymentMethodRegistrationFailure are less correlated with fraud column and thus not contribute to our model accuracy."""

# therefore removing
# all above columns 

lis=["No_Transactions","transactionFailed","paymentMethodType","paymentMethodRegistrationFailure",""]

for i in lis:
  df3=df3.drop([i],axis=1)

sns.heatmap(df3.corr(),cmap="coolwarm")
df3.corr()

sns.countplot(df3["Fraud"])

plt.hist(df3["Fraud"])

sns.barplot(df3["orderState"],df3["Fraud"])

df3.hist(figsize=(20,20))

"""**FRAUD DETECTION WITH ML MODELS**
**i.e. TRAINING AND TESTING WITH ML MODELS**
"""

x=df3.iloc[:,0:4]
y=df3.iloc[:,4:5]
from sklearn.model_selection import train_test_split

x.head()

y.head()

x_train, x_val, y_train, y_val = train_test_split(x, y, test_size = 0.2, random_state = 40)

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()

x_train=sc.fit_transform(x_train)
x_val=sc.transform(x_val)

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

gaussian = GaussianNB()
gaussian.fit(x_train, y_train)
y_pred = gaussian.predict(x_val)
acc_gaussian = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_gaussian)

from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()
logreg.fit(x_train, y_train)
y_pred = logreg.predict(x_val)
acc_logreg = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_logreg)

from sklearn.svm import SVC

svc = SVC(gamma="auto")
svc.fit(x_train, y_train)
y_pred = svc.predict(x_val)
acc_svc = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_svc)

from sklearn.svm import LinearSVC

linear_svc = LinearSVC()
linear_svc.fit(x_train, y_train)
y_pred = linear_svc.predict(x_val)
acc_linear_svc = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_linear_svc)

from sklearn.tree import DecisionTreeClassifier

decisiontree = DecisionTreeClassifier()
decisiontree.fit(x_train, y_train)
y_pred = decisiontree.predict(x_val)
acc_decisiontree = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_decisiontree)

from sklearn.ensemble import RandomForestClassifier

randomforest = RandomForestClassifier(n_estimators=35)
randomforest.fit(x_train, y_train)
y_pred = randomforest.predict(x_val)
acc_randomforest = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_randomforest)

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier()
knn.fit(x_train, y_train)
y_pred = knn.predict(x_val)
acc_knn = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_knn)

from sklearn.linear_model import SGDClassifier

sgd = SGDClassifier()
sgd.fit(x_train, y_train)
y_pred = sgd.predict(x_val)
acc_sgd = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_sgd)

from sklearn.ensemble import GradientBoostingClassifier

gbc = GradientBoostingClassifier()
gbc.fit(x_train, y_train)
y_pred = gbc.predict(x_val)
acc_gbc = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_gbc)

# confusion_matrix for
# decisiontreeclassifier

from sklearn.metrics import confusion_matrix
confusion_matrix(y_pred,y_val)

sns.heatmap(confusion_matrix(y_pred,y_val),cmap="coolwarm")

"""**FROM ABOVE ALL TRAINED MODELS WE OBSERVE THAT DecisionTreeClassifier WORKS BETTER IN TERMS OF ACCURACY WITH ACCURACY OF 85.37%**"""

