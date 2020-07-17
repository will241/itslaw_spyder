import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


data = pd.read_csv(r'./data.csv')
X = data.drop(['charge_time'], axis=1)
y = data['charge_time']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2020, test_size=0.3)

# 1
lr = LinearRegression()
lr.fit(X_train, y_train.values.ravel())
score = lr.score(X_test, y_test)
print('线性回归模型预测结果为：{0}'.format(str(score)))


# 2
knn = KNeighborsClassifier()
knn.fit(X_train, y_train.values.ravel())
score = knn.score(X_test, y_test)
print('K最临近算法预测结果为：{0}'.format(str(score)))
