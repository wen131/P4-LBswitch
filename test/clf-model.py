import numpy
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import random

with open("data60","r") as f:
  data=f.read()
  data=data.split("\n")

x=numpy.array([[sum(list(map(lambda x:float(x),data[i].split(" ")[:3])))/3, data[i].split(" ")[3]] for i in range(len(data)-1)])
y=numpy.array([float(data[i].split(" ")[-1]) for i in range(len(data)-1)])
print(x)

clf=Pipeline([('poly', PolynomialFeatures(degree=20)),('linear', linear_model.Ridge())])
clf.fit(x,y)

print(clf.predict([[1,i] for i in range(10,40)]))
print(clf.predict([[i/50,19] for i in range(20,40)]))

a=0
for i in range(len(y)):
  a+=(clf.predict(x[i]).take(0)>0.7*y[i]) and (clf.predict(x[i]).take(0)<1.3*y[i])
print(a/len(y))
