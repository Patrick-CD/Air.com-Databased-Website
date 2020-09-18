# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:53:12 2020

@author: zhu
"""

import datetime
from datetime import timedelta
import  time

#获取当前日期
today=time.strftime('%Y-%m-%d',time.localtime(time.time()))

str=today.replace("-","")
str2date=datetime.datetime.strptime(str,"%Y%m%d")#字符串转化为date形式
a = str2date-timedelta(30)
print(a)

#根据给定的日期，获取前n天或后n天的日期，n为正数则是以后的n天，n为负数则是以前的n天
def get_day_of_day(str2date,n=0):
    if(n<0):
        n = abs(n)
        return (str2date-timedelta(days=n))
    else:
        return str2date+timedelta(days=n)

i=0
while(True):
    i-=1
    getDate=get_day_of_day(str2date, i).date().strftime("%Y-%m-%d")
    time.sleep(1)
    print(getDate)
    endDate="2019-02-04"
    if(getDate==endDate):
        break
j=0
while(True):
    j+=1
    getDate = get_day_of_day(str2date, j).date().strftime("%Y-%m-%d")
    time.sleep(1)
    print(getDate)
    endDate = "2019-03-20"
    if (getDate == endDate):
        break
