# -*- coding: utf-8 -*-
"""HeartDisease.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pP_575eVtm79mV6wMApaUErHGaRhw_PR
"""

import pandas as pd
heart = pd.read_csv('heart.csv')

#데이터셋 10개 샘플 확인
#HeartDisease : 0/1 -> 심장병인지 아닌지 골라내는 문제
#0 음성 / 1 양성
heart.head(10)

#누락된 데이터 확인
heart.info()
#누락된 데이터 없음

heart.shape

#통계 추출
heart.describe()

#넘파이 배열
data = heart[['Age', 'RestingBP', 'Cholesterol','FastingBS', 'MaxHR','Oldpeak']].to_numpy()
target = heart['HeartDisease'].to_numpy()

#훈련 세트, 테스트 세트
#테스트 개수 270개
from sklearn.model_selection import train_test_split
train_input, test_input, train_target, test_target = train_test_split(data, target, test_size=270)

#훈련 세트, 테스트 세트 크기 확인
print(train_input.shape, test_input.shape)

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
ss.fit(train_input)
train_scaled = ss.transform(train_input)
test_scaled = ss.transform(test_input)

#로지스틱 회귀 모델 훈련
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(train_scaled, train_target)

print(lr.score(train_scaled, train_target))
print(lr.score(test_scaled, test_target))

"""-> 점수가 높지 않음! : 모델 과소적합 예상"""

print(lr.coef_, lr.intercept_)

#결정 트리
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(random_state=42)
tree.fit(train_scaled, train_target)
print(tree.score(train_scaled, train_target))#훈련
print(tree.score(test_scaled, test_target))#테스트

"""훈련 세트 점수 1;;
테스트 성능은 훈련 세트보다 낮음 : 과대적합 모델
"""

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
plt.figure(figsize=(10,7))
plot_tree(tree)
plt.show()

#트리 깊이 제한
plt.figure(figsize=(10,7))
plot_tree(tree, max_depth=1, filled=True, feature_names=['Age', 'RestingBP', 'Cholesterol','FastingBS', 'MaxHR','Oldpeak'])
plt.show()

"""설명 추가 예정
불순도 : 0.497
"""

print(tree.feature_importances_)

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(train_input, train_target)
print(tree.score(train_input, train_target))
print(tree.score(test_input, test_target))

plt.figure(figsize=(20,15))
plot_tree(tree, filled=True, feature_names=['Age', 'RestingBP', 'Cholesterol','FastingBS', 'MaxHR','Oldpeak'])
plt.show()