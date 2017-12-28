#!/usr/bin/python3
# coding: utf-8
# 上面两句注释必须要，防止无法打印中文的

import datetime
import os
import re
from pyquery import PyQuery as pq
import pymysql.cursors
import requests

date_of_today = datetime.datetime.now().strftime("%Y-%m-%d")
# os.mknod(date_of_today)
date_of_today='2014-12-29'#items = doc('')
data_threedays = []  # 保存三日龙虎榜的list
data_not3day = []


class Info_unit(object):
    """docstring for info_unit"""
    def __init__(self, item):
        self.__stock_code = item('.stockcont').attr('stockcode')  # 抓取股票代码
        self.__rid = item('.stockcont').attr('rid')  # 抓取上榜编号 可以判断出上榜理由
        self.__title = item('p').html()  # 抓取股票名字
        self.__reason = (self.__title).split(u'：')[1]  # 汉字使用Unicode编码，以u表示出来
        self.__title = (self.__title).split('(')[0]
        # print(item('.cjmx')('p')('span').text()+'wanyuan')
        self.__totall_buy_in = item('.cjmx')('p')('span').html()
        self.__totall_sell_out = item('.cjmx')('p')('span')('.c-fall').html()
        # print(self.__totall_buy_in,'&&&&&&&',self.__totall_sell_out)

        # self.data = []  # 保存每个股票的十位营业部、买入额、卖出额
        
        self.data_buy = self.__tr_xiwei(item('tbody').eq(0)('tr').items()) #保存买前五的数组
        self.data_sell = self.__tr_xiwei(item('tbody').eq(1)('tr').items())

        self.stockcont = {'stock_code': self.__stock_code, 'rid': self.__rid,  'name': self.__title, 'reason': self.__reason,
                          'totall_buy_in': self.__totall_buy_in, 'totall_sell_out': self.__totall_sell_out,
                          'buyers': self.data_buy, 'sellers': self.data_sell, 'date_in': date_of_today}
        self.is_3days()

    def is_3days(self):  # 判断是否3日上榜,不在字典中则为当日
        rid = self.__rid.split('_')[1]
        tf = {'7': True, '8': True, '10': True, '11': True,
              '28': True, '29': True}.get(rid, False)
        if tf:  # 如果为true表示三日的
            print('is_3days', self.stockcont['rid'], self.stockcont['name'])
            data_threedays.append(self.get_dict())
        else:
            # print('not_3days', self.stockcont['rid'], self.stockcont['name'])
            data_not3day.append(self.get_dict())
            # print(len(data_not3day))
        pass

    def get_dict(self):
        return self.stockcont
        pass
#__tr_xiwei()函数：提取传入的<tbody>下的五个<tr>,每次调用该函数会循环五次;返回保存五个席位的list,如下:
# return [['华泰证券股份有限公司上海浦东新区福山路证券营业部', '5158.49', '89.30'], [同前面],[],[],[]]
    def __tr_xiwei(self, trs):
        # sub_data_gen=[tr('a').attr('title') for tr in trs]
        buy_sell = []
        for tr in trs:
            # print(tr.text()) #排查网页编码错误使用，勿删
#             sub_data = []  # 缓存每个股票的十位营业部、买入额、卖出额
#             # 席位营业部 tr.children().eq(0).text()
#             sub_data.append(tr('a').attr('title'))
# #			print(tr.children().eq(0).text())
#             sub_data.append(tr.children().eq(1).text())  # 买入金额
#             sub_data.append(tr.children().eq(2).text())  # 卖出金额
#             # self.data.append(sub_data)
#             buy_sell.append(sub_data)

            sub_data_dic={'bs_name':0,'buy_value':0,'sell_value':0}
            sub_data_dic['bs_name']=tr('a').attr('title')
            # sub_data_dic['buy_value']=tr.children().eq(1).text()
            # sub_data_dic['sell_value']=tr.children().eq(2).text()    
            # print(tr.text().split(' '))     
            sub_data_dic['buy_value']=tr.text().split(' ')[-3]
            sub_data_dic['sell_value']=tr.text().split(' ')[-2]
            buy_sell.append(sub_data_dic)
        return buy_sell

    def save_to_db(self):  # 存入MySQL数据库 mysql密码为root Cjf1991cjf!
        cnx = pymysql.connect(user='root', password='Cjf1991cjf!',
                              host='127.0.0.1', database='tonghuashun', charset="utf8")
        cursor = cnx.cursor()
        print('--------------------------------------------------')
        # print(self.data)
        for i in self.data_buy+self.data_sell:
            # add_data = ("INSERT INTO stocks (code, rid, name, reason, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out,date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s ,%s ,%s,%s  )")
            add_data = ("INSERT INTO stocks1 (stock_code, rid, name, reason, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out,date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s ,%s ,%s,%s  )")
#			data_data = (self.stock_code, self.rid,self.title ,i[0],i[1],i[2])
            # print(i)
            data_data = (self.__stock_code, self.__rid, self.__title, self.__reason,
                         self.__totall_buy_in, self.__totall_sell_out, i[0], i[1], i[2], date_of_today)
            cursor.execute(add_data, data_data)
            cnx.commit()
        cursor.close()
        cnx.close()

    def test(self):
        for x in self.stockcont['buyers']:
            print(self.stockcont['stock_code'], self.stockcont['rid'], self.stockcont['name'], self.stockcont['reason'],
                  self.stockcont['totall_buy_in'], self.stockcont['totall_sell_out'],
                  x[0], x[1], x[2], self.stockcont['date_in'])
            print('--------------------------------------------------')
        pass

def getDate(i,j):
    year='2017'
    mon=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    day=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    date_of_today=year+'-'+mon[i-1]+'-'+day[j-1]
    return date_of_today

# doc = pq(url='http://data.10jqka.com.cn/market/longhu/')

# date_of_today=getDate(12,12)
URL = 'http://data.10jqka.com.cn/ifmarket/lhbggxq/report/'+date_of_today
head = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0) ',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html, application/xhtml+xml, */*', 'Cookie': ''}
r = requests.get(URL, headers=head)
print('--------------------')
# print("响应头", r.headers)
# print("请求头", r.request.headers)
# doc = pq(filename='out.txt',encoding="utf-8")
luanMa=re.compile(u'[\U00000000]') #不影响效率的情况下尽量把00-1F过滤掉，属于不可见字符；
tt=luanMa.sub(u'',r.text)
# fileout=open('out.txt','w',encoding="utf-8");
# fileout.write(tt+'\n')
# fileout.close()
print(tt)
doc = pq(tt, parser='html')
print(doc.html())
try:
    items = doc('.rightcol.fr')('.stockcont').items()
except Exception as e:
    print('没有连网！！！')
else:
    print('已连网抓到网页，继续进行！！！')
# item('tbody')与item('tbody').items()有很大区别：需要使用for循环遍历时候用.items()；需要继续用pyquery选择器选择DOM时不加.items()
#.items() 将pyquery对象格式化为python的对象【个人理解】
i = 0
start_time = datetime.datetime.now()

for item in items:  # 遍历每个个股
    stock = Info_unit(item)
    # stock.save_to_db()
    # data_not3day.append(stock.get_dict())
    i = i+1

def save_to_db_once(list_all): #这个写mysql的方法比上面的效率高
    cnx = pymysql.connect(user='root', password='Cjf1991cjf!',
                      host='127.0.0.1', database='tonghuashun', charset="utf8")
    cursor = cnx.cursor()
    add_data = ("INSERT INTO stocks (code, rid, name, reason, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out,date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s ,%s ,%s,%s  )")
    # add_data = ("INSERT INTO stocks1 (stock_code, rid, name, reason, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out,date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s ,%s ,%s,%s  )")
    print('--------------------------------------------------')
    for dic in list_all:
        for bs in dic['buyers']+dic['sellers']:
            data_data = (dic['stock_code'], dic['rid'], dic['name'], dic['reason'],
                        dic['totall_buy_in'], dic['totall_sell_out'], bs['bs_name'], bs['buy_value'], bs['sell_value'], date_of_today)
            cursor.execute(add_data, data_data)
            # print(bs)
    print('准备提交<龙虎榜详情数据>到数据库')
    cnx.commit() #循环外一次提交效率搞很多倍
    cursor.close()
    cnx.close()

# buy_all=0;buy_num=0;sell_all=0;sell_num=0

def map_arr(data_dic,res):
    for bs in data_dic['buyers']+data_dic['sellers']:
        if float(bs['sell_value'])>1000 :
            res['sell_all']=res['sell_all']+float(bs['sell_value'])
            res['sell_num']=res['sell_num']+1
        if float(bs['buy_value'])>1000:
            res['buy_all']=res['buy_all']+float(bs['buy_value'])
            res['buy_num']=res['buy_num']+1
        pass
    return res
def xunhuan(datas): #循环数组统计非三天的大于1000万的额度，返回result字典
    res={'buy_all':0,'buy_num':0,'sell_all':0,'sell_num':0}
    for data in datas:
        map_arr(data,res)
    pass
    res['buy_all']=round(res['buy_all'],2)
    res['sell_all']=round(res['sell_all'],2)
    return res
def save_once(result): #这个写mysql的方法比上面的效率高
    cnx = pymysql.connect(user='root', password='Cjf1991cjf!',
                      host='127.0.0.1', database='tonghuashun', charset="utf8")
    cursor = cnx.cursor()
    add_data = ("INSERT INTO lhb_avg ( buy_all,buy_num,   sell_all,sell_num,buy_avg,sell_avg, date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s )")
    print('--------------------------------------------------')
    b_avg=round(result['buy_all']/result['buy_num'],2)
    s_avg=round(result['sell_all']/result['sell_num'],2)
    print('买入大于1000万平均值：',b_avg,'卖出大于1000万平均值：',s_avg)
    data_data = (result['buy_all'],result['buy_num'],result['sell_all'],result['sell_num'],b_avg,s_avg,date_of_today)
    print('准备提交<上榜平均额>到数据库')
    cursor.execute(add_data, data_data)
    cnx.commit() #循环外一次提交效率搞很多倍
    cursor.close()
    cnx.close()

# start = datetime.datetime.now()
result=xunhuan(data_not3day)
# save_to_db_once(data_not3day+data_threedays) #写入数据库：上榜详情
# save_once(result) #写入数据库：上榜平均额
end_time = datetime.datetime.now()
print("插入数据库消耗时间：Cast: ",(end_time-start_time).microseconds/1000,"ms")
print('Done！！！')
print('--------------------------------------------------')
print("今日总共上榜股票个数：",i)
print('今日上榜数量：',len(data_not3day),' 三日上榜数量：',len(data_threedays))
print(result)
print('买入平均值：',round(result['buy_all']/result['buy_num'],2),'卖出平均值：',round(result['sell_all']/result['sell_num'],2))
print('--------------------------------------------------')

def reduce_sum():
    pass
# map(map_arr, data_not3day)
# reduce(reduce_sum, sequence)