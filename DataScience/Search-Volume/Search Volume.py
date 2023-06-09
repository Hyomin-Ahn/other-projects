# -*- coding: utf-8 -*-
"""검색량추이.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HdodZtcUR5il2eqRtMz4_QbqBjNSMlql
"""

!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf

import urllib.request
import json
import pandas as pd
import re

client_id = "0rkYGd8XkcgitqaQTvRr"
client_secret = "yn6_JnO7JE"

url = "https://openapi.naver.com/v1/datalab/search"
body = '''{"startDate":"2021-06-01","endDate":"2022-11-30","timeUnit":"month",
          "keywordGroups":[{"groupName":"자립준비청년",  "keywords":["자립준비청년", 
          "보호종료아동", "자립준비 청년"]}]
          }'''

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", "0rkYGd8XkcgitqaQTvRr")
request.add_header("X-Naver-Client-Secret", "yn6_JnO7JE")
request.add_header("Content-Type","application/json")
response=urllib.request.urlopen(request, data=body.encode("utf-8"))
rescode = response.getcode()

if(rescode==200):
  response_body = response.read()
  query=response_body.decode('utf-8')
  data_query=json.loads(query)
else:
  print("Error Code:" + rescode)

#데이터 전처리
dates = []
agedOutOrphans_query=[]
for i in data_query['results'][0]['data']:
  dates.append(i['period'])
  agedOutOrphans_query.append(i['ratio'])

df=pd.DataFrame([dates, agedOutOrphans_query]).T
df.columns=['Date', 'ageout']

import datetime
df['Date']=df['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
df['Date']=df['Date'].apply(lambda x: x.strftime('%y%m'))


df['ageout']=df['ageout'].astype(int)

import matplotlib.pyplot as plt

plt.rc('font', family='NanumBarunGothic') 
plt.rc('font', size=12)
plt.figure(figsize=(16,12))

plt.plot(df['Date'], df['ageout'])
for i in range(len(df)):
  plt.text(i, df['ageout'][i], df['ageout'][i], fontsize=8, 
           horizontalalignment='center', verticalalignment='bottom')

plt.legend(['검색량'], loc='upper left')
plt.title('자립준비청년 검색량 추이')

