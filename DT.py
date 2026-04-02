#DT model implementation
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

data = pd.read_csv('C:\\Users\\harsh\\.vscode\\.venv\\Iris.csv')
data
x = data.iloc[:,1:5]
y = data.iloc[:,5]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 42)
print(x_train.shape)
print(y_train.shape)

dmodel = DecisionTreeClassifier(criterion='entropy',random_state=42)
dmodel.fit(x_train,y_train)
y_pred = dmodel.predict(x_test)
print(y_pred)
print(y_test)
print(accuracy_score(y_pred,y_test))
print(confusion_matrix(y_pred,y_test))