#Linear Regression model

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
data = pd.read_csv('C:/Users/harsh/OneDrive/Desktop/ToyotaCorolla (1).csv')

print(data.head())
print(data.count())
print(data.isnull().sum())
x = data.drop('Price', axis=1).values
x = data.drop('FuelType', axis=1).values
y = data.iloc[:,0].values.reshape(-1,1)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 15)
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)
from sklearn.linear_model import LinearRegression
regression_linear = LinearRegression()
regression_linear.fit(x_train,y_train)
y_pred = regression_linear.predict(x_test)
ms = mean_squared_error(y_test,y_pred)
print(ms)
plt.plot(y_test,y_pred,color = 'green',linewidth=20)
