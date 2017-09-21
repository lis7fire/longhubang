#!/usr/bin/python3
#coding: utf-8
# 上面两句注释必须要，防止无法打印中文的

import datetime
import os
from pyquery import PyQuery as pq
import pymysql.cursors

date_of_today = datetime.datetime.now().strftime("%Y-%m-%d")
#os.mknod(date_of_today)
#date_of_today='2017-05-11'#items = doc('')

class Info_unit(object):
	"""docstring for info_unit"""
	def __init__(self, item):
		self.stock_code = item('.stockcont').attr('stockcode') #抓取股票代码
		self.rid = item('.stockcont').attr('rid')  #抓取上榜编号 这里要处理数据
		self.title = item('p').html() #抓取上榜类型，需要处理
		self.reason=(self.title).split(u'：')[1] #汉字使用Unicode编码，以u表示出来
		self.title=(self.title).split('(')[0]
		print(item('.cjmx')('p')('span').text()+'wanyuan')
		self.totall_buy_in = item('.cjmx')('p')('span').html()
		self.totall_sell_out = item('.cjmx')('p')('span')('.c-fall').html()
		print(self.totall_buy_in,'&&&&&&&',self.totall_sell_out)
		self.data = [] #保存每个股票的十位营业部、买入额、卖出额
		self.data_threedays= [] #保存三日龙虎榜的list
		self.data_buy=[]
		self.data_sell=[]

		tbodys=item('tbody').items()
		self.tiqu_tbody(tbodys)

		# if : #可以模块独立出来，在这里判断如果是三日的榜单就排到另外一个list中：
		# 	pass
		# trs = item('tr:not(.bg-blue)').items()
		print('-----------',i+1,self.stock_code,self.title,self.reason,'---------------------------------------')
		# self.tiqu(trs)
		# print(self.data)
#		self.save_to_db()

	def tiqu_tbody(self,tbodys):
		xx=True
		for tb in tbodys:
			if xx:
				print('================买入：===================')
				# print(tb.html())
				self.data_buy=self.tiqu(tb('tr').items())
				xx=False
				print('买入是：',self.data_buy)
				pass
			else:
				print('================卖出：===================')
				self.data_sell=self.tiqu(tb('tr').items())
				print('卖出是：',self.data_sell)
				# print(tb.html())
		pass

	def tiqu(self,trs):#提取一个股票的买入前五和卖出前五，总共十个
		# sub_data_gen=[tr('a').attr('title') for tr in trs]
		buy_sell=[]
		for tr in trs:
			sub_data = []
			sub_data.append(tr('a').attr('title')) #席位营业部 tr.children().eq(0).text()
#			print(tr.children().eq(0).text())
			sub_data.append(tr.children().eq(1).text()) #买入金额
			sub_data.append(tr.children().eq(2).text()) #卖出金额
			# print('sub_data是：',sub_data)
			# self.data.append(sub_data)
			buy_sell.append(sub_data)
		return buy_sell

	def save_to_db(self): #存入MySQL数据库
		cnx = pymysql.connect(user='root',password='Cjf1991cjf!',host='localhost',database='tonghuashun', charset="utf8")
		cursor = cnx.cursor()
		for i in self.data:
#			add_data = ("INSERT INTO stocks (code, rid, name, reason, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out,date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s ,%s ,%s,%s  )")
			add_data = ("INSERT INTO stocks1 (stock_code, rid, name, reason, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out,date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s ,%s ,%s,%s  )")
#			data_data = (self.stock_code, self.rid,self.title ,i[0],i[1],i[2]) 
			print(i)
			data_data = (self.stock_code, self.rid,self.title ,self.reason,self.totall_buy_in,self.totall_sell_out,i[0],i[1],i[2],date_of_today) # 
			cursor.execute(add_data, data_data)
			cnx.commit()
		cursor.close()
		cnx.close()

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

print('Done！！！' )
print(i) 
