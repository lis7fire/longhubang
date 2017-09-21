#!/usr/bin/env python3
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
		self.__stock_code = item('.stockcont').attr('stockcode') #抓取股票代码
		self.__rid = item('.stockcont').attr('rid')  #抓取上榜编号 这里要处理数据
		self.__title = item('p').html() #抓取上榜类型，需要处理
		self.__reason=(self.__title).split(u'：')[1] #汉字使用Unicode编码，以u表示出来
		self.__title=(self.__title).split('(')[0]
		print(item('.cjmx')('p')('span').text()+'wanyuan')

		self.__totall_buy_in = item('.cjmx')('p')('span').html()
		self.__totall_sell_out = item('.cjmx')('p')('span')('.c-fall').html()
		print(self.__totall_buy_in,'&&&&&&&',self.__totall_sell_out)

		self.data = [] #保存每个股票的十位营业部、买入额、卖出额
		self.data_threedays= [] #保存三日龙虎榜的list
		# if :# 可以模块独立出来，在这里判断如果是三日的榜单就排到另外一个list中：
		# 	pass	
		trs = item('tr:not(.bg-blue)').items()
		print('-----------',i+1,self.__stock_code,self.__title,self.__reason,'---------------------------------------')
		self.tiqu(trs)

		self.stockcont=	{'stock_code':self.__stock_code,   'rid':self.__rid,  'name':self.__title , 
		'reason': self.__reason,  'totall_buy_in':self.__totall_buy_in, 'totall_sell_out':self.__totall_sell_out, 
		'buyers':self.data, 'date_in':date_of_today}
		
		print(self.stockcont)
#		self.save_to_db()

	def tiqu(self,trs):#提取一个股票的买入前五和卖出前五，总共十个
		for tr in trs:
			sub_data = []
			sub_data.append(tr('a').attr('title')) #席位营业部 tr.children().eq(0).text()
#			print(tr.children().eq(0).text())
			sub_data.append(tr.children().eq(1).text()) #买入金额
			sub_data.append(tr.children().eq(2).text()) #卖出金额
			self.data.append(sub_data)
			print(sub_data)

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