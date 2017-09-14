#!/usr/bin/python  
#-*-coding:utf-8-*- 
# 上面两句注释必须要，防止无法打印中文的

from __future__ import print_function
import datetime
import os
from pyquery import PyQuery as pq
import mysql.connector

date_of_today = datetime.datetime.now().strftime("%Y-%m-%d")
#os.mknod(date_of_today)
#date_of_today='2017-05-23'

class Info_unit(object):
	"""docstring for info_unit"""
	def __init__(self, item):
		self.stock_code = item('.stockcont').attr('stockcode') #抓取股票代码
		self.rid = item('.stockcont').attr('rid')  #抓取上榜编号 这里要处理数据
		self.title = item('p').html() #抓取上榜类型，需要处理
		self.reason=(self.title).split(u'：')[1] #汉字使用Unicode编码，以u表示出来
		self.title=(self.title).split('(')[0]

		span = item('.cjmx')('p')('span').items()
		print(item('.cjmx')('p')('span').text()+'wanyuan')

#		print(item('.cjmx')('p')('span')('.c-fall').html())
		self.totall_buy_in = span.next().html()
		self.totall_sell_out = span.next().html()
		self.data = []
		trs = item('tr:not(.bg-blue)').items()
		for tr in trs:
			cnx = mysql.connector.connect(user='root',password='Cjf1991cjf!',host='localhost',database='tonghuashun')
			cursor = cnx.cursor()			
			sub_data = []
			sub_data.append(tr('a').html()) #席位营业部 tr.children().eq(0).text()
#			print(tr.children().eq(0).text())
			sub_data.append(tr.children().eq(1).text()) #买入金额
			sub_data.append(tr.children().eq(2).text()) #卖出金额
			self.data.append(sub_data)
#			print(sub_data[0])

			add_data = ("INSERT INTO stocks (code, rid, name, reason, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out,date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s ,%s ,%s,%s  )")
#			add_data = ("INSERT INTO stocks1 (stock_code, rid ) VALUES (%s, %s )")
			
#			data_data = (self.stock_code, self.rid) # tr('a').html(), tr('.c-rise').html() ,tr('.c-fall').html()
			data_data = (self.stock_code, self.rid,self.title, self.reason,self.totall_buy_in,self.totall_sell_out,sub_data[0],sub_data[1],sub_data[2],date_of_today) # tr('a').html(), tr('.c-rise').html() ,tr('.c-fall').html()
			cursor.execute(add_data, data_data)
			cnx.commit()
			cursor.close()
			cnx.close()

	# def save_to_db():
	# 	cnx = mysql.connector.connect(user='root',password='Cjf1991cjf!',host='127.0.0.1',database='stock')
	# 	cursor = cnx.cursor()
	# 	for tr in trs:
	# 		add_data = ("INSERT INTO stocks (stock_code, title, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out) VALUES (%s, %s, %s, %s, %s)")
	# 		data_data = (self.stock_code, self.title, self.totall_buy_in, self.totall_sell_out, tr('a').html(), tr('.c-rise').html() ,tr('.c-fall').html())	
	# 		cursor.execute(add_data, data_data)
	# 		cnx.commit()
	# 	cursor.close()
	# 	cnx.close()		

doc = pq('http://data.10jqka.com.cn/market/longhu/')
#doc = pq(filename='downlhb.html', parser='html')

# rightcol = doc('.rightcol fr') # 获取龙虎榜部分 
# items = rightcol('.stockcont').items() # 获取个股的龙虎榜
items = doc('.rightcol')('.stockcont').items()
instances = []
i=0
for item in items: # 遍历每个个股
	instances.append(Info_unit(item))
	i=i+1
#	print(item)

print('Done' )
print(i) 
