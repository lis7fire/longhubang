#!/usr/bin/python  
#-*-coding:utf-8-*- 
# 上面两句注释必须要，防止无法打印中文的

from __future__ import print_function
import datetime
import os
import mysql.connector

date_of_today = datetime.datetime.now().strftime("%Y-%m-%d")
#os.mknod(date_of_today)
#date_of_today='2017-05-23'
i=0;j=0
SELECT=('count','distinct sum') 
BUY_SELL=('buy_in','sell_out')
#print(SELECT[i],BUY_SELL[j])

sql=date_of_today+'" and rid not like "%_7" and rid not like "%_8" and rid not like "%_10" and rid not like "%_11" and rid not like "%_28" and rid not like "%_29" and '
#SQL_NUM ='select count(*) from stocks where date_in= " %s %s > 1000 ' % (sql,BUY_SELL[j]) 
#SQL_ALL ='select distinct sum(%s) from stocks where date_in= " %s %s > 1000 ' % (BUY_SELL[j],sql,BUY_SELL[j]) 
#SQLS=[SQL_NUM,SQL_ALL]

buy_num=0;sell_num=0;buy_all=0;sell_all=0;
ziduan=[[buy_num, sell_num], [buy_all,sell_all]]

cnx = mysql.connector.connect(user='root',password='Cjf1991cjf!',host='localhost',database='tonghuashun')
cursor = cnx.cursor()

for i in range(0,2):
	SQLHEAD ='select %s' % (SELECT[i])
	for j in range(0,2):
		SQL ='%s(%s) from stocks where date_in= " %s  %s > 1000 ' % (SQLHEAD,BUY_SELL[j],sql, BUY_SELL[j])
		print(SQL)
		cursor.execute(SQL)
		for num in cursor:  
			ziduan[i][j]=num[0]
		j+=1
	i+=1

buy_avg=format(ziduan[1][0]/ziduan[0][0],'.2f')
sell_avg=format(ziduan[1][1]/ziduan[0][1],'.2f')
add_data = ("INSERT INTO lhb_avg (buy_avg, buy_num, buy_all, sell_avg, sell_num, sell_all, date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s )")			
data_data = (buy_avg, ziduan[0][0],ziduan[1][0], sell_avg,ziduan[0][1],ziduan[1][1],date_of_today) # tr('a').html(), tr('.c-rise').html() ,tr('.c-fall').html()
print(buy_avg, ziduan[0][0],ziduan[1][0], sell_avg,ziduan[0][1],ziduan[1][1],date_of_today)

cursor.execute(add_data, data_data)
#cnx.commit()
cursor.close()
cnx.close()
print(buy_num,buy_all, sell_num, sell_all)
print(ziduan[0][0],ziduan[1][0],ziduan[0][1],ziduan[1][1],)
print('Done' )
