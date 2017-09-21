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
		self.__stock_code = item('.stockcont').attr('stockcode') #抓取股票代码
		self.__rid = item('.stockcont').attr('rid')  #抓取上榜编号 可以判断出上榜理由
		self.__title = item('p').html() #抓取股票名字
		self.__reason=(self.__title).split(u'：')[1] #汉字使用Unicode编码，以u表示出来
		self.__title=(self.__title).split('(')[0]
		# print(item('.cjmx')('p')('span').text()+'wanyuan')
		self.__totall_buy_in = item('.cjmx')('p')('span').html()
		self.__totall_sell_out = item('.cjmx')('p')('span')('.c-fall').html()
		# print(self.__totall_buy_in,'&&&&&&&',self.__totall_sell_out)

		self.data = [] #保存每个股票的十位营业部、买入额、卖出额
		self.data_threedays= [] #保存三日龙虎榜的list

		self.data_buy=self.tr_xiwei(item('tbody').eq(0)('tr').items())
		self.data_sell=self.tr_xiwei(item('tbody').eq(1)('tr').items())	
		self.is_3days()
		self.stockcont=	{'stock_code':self.__stock_code,   'rid':self.__rid,  'name':self.__title , 
		'reason': self.__reason,  'totall_buy_in':self.__totall_buy_in, 'totall_sell_out':self.__totall_sell_out, 
		'buyers':self.data_buy,'sellers':self.data_sell, 'date_in':date_of_today}
		# print(self.__rid)
		# self.test()
#		self.save_to_db()

	def is_3days(self):#判断是否3日上榜
		rid=self.__rid.split('_')[1]
		tf={'3':False, '4':False, '6':False, '7':True, '306':False, '406':False, '13032':False,}[rid]
		if tf:#如果为true表示三日的
			print('is_3days',self.stockcont['name'])
			pass
		pass

	def get_dict(self):
		return self.stockcont
		pass
#tr_xiwei()函数：提取传入的<tbody>下的五个<tr>,每次调用该函数会循环五次;返回保存五个席位的list,如下:
#return [['华泰证券股份有限公司上海浦东新区福山路证券营业部', '5158.49', '89.30'], [同前面],[],[],[]]
	def tr_xiwei(self,trs):
		# sub_data_gen=[tr('a').attr('title') for tr in trs]
		buy_sell=[]
		for tr in trs:
			sub_data = []#缓存每个股票的十位营业部、买入额、卖出额
			sub_data.append(tr('a').attr('title')) #席位营业部 tr.children().eq(0).text()
#			print(tr.children().eq(0).text())
			sub_data.append(tr.children().eq(1).text()) #买入金额
			sub_data.append(tr.children().eq(2).text()) #卖出金额
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

	def test(self):
		for x in self.stockcont['buyers']:
			print(self.stockcont['stock_code'], self.stockcont['rid'],self.stockcont['name'],
				self.stockcont['reason'],self.stockcont['totall_buy_in'] , self.stockcont['totall_sell_out'],
				x[0],x[1],x[2],self.stockcont['date_in']) 
			print('--------------------------------------------------')
		pass

doc = pq('http://data.10jqka.com.cn/market/longhu/')
#doc = pq(filename='downlhb.html', parser='html')

items = doc('.rightcol.fr')('.stockcont').items()
#item('tbody')与item('tbody').items()有很大区别：需要使用for循环遍历时候用.items()；需要继续用pyquery选择器选择DOM时不加.items()
#.items() 将pyquery对象格式化为python的对象【个人理解】
instances = []
i=0
for item in items: # 遍历每个个股
	instances.append(Info_unit(item).get_dict())
	i=i+1
	# if i==5:#测试用
	# 	break
# print(instances)

print('Done！！！' )
print(i) 
