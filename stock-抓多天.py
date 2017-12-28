#!/usr/bin/python3
# coding: utf-8
# 上面两句注释必须要，防止无法打印中文的

from datetime import datetime, date
import os
import re
import logging
import traceback
from pyquery import PyQuery as pq
from collections import Iterator
import pymysql.cursors
import requests

# date_of_today = datetime.now().strftime("%Y-%m-%d")
# os.mknod(date_of_today)
date_of_today = '2017-12-28'  # 第一次有数据的日期：'2014-06-04'
data_threedays = []  # 保存三日龙虎榜的list
data_not3day = []
count = 0


class Info_unit(object):  # 用于抓取网页并解析的类
    """docstring for info_unit"""

    def __init__(self):
        print('Info_unit类初始化。。。')

    def jieXi(self, item):
        self.__stock_code = item('.stockcont').attr('stockcode')  # 抓取股票代码
        self.__rid = item('.stockcont').attr('rid')  # 抓取上榜编号 可以判断出上榜理由
        self.__title = item('p').html()  # 抓取股票名字
        self.__reason = (self.__title).split(u'：')[1]  # 汉字使用Unicode编码，以u表示出来
        self.__title = (self.__title).split('(')[0]
        # print(item('.cjmx')('p')('span').text()+'wanyuan')
        self.__totall_buy_in = item('div.cell-cont.cjmx')('p span').html()
        self.__totall_sell_out = item('.cjmx')('p')('span.c-fall').html()
        # print(self.__totall_buy_in,'&&&&&&&',self.__totall_sell_out)

        self.data_buy = self.__tr_xiwei(item('tbody').eq(0)('tr').items())  # 保存买前五的数组；营业部、买入额、卖出额
        self.data_sell = self.__tr_xiwei(item('tbody').eq(1)('tr').items())

        self.stockcont = {"stock_code": self.__stock_code, "rid": self.__rid, "name": self.__title,
                          "reason": self.__reason,
                          "totall_buy_in": self.__totall_buy_in, "totall_sell_out": self.__totall_sell_out,
                          "buyers": self.data_buy, "sellers": self.data_sell, "date_in": date_of_today}

    def is_3days(self):  # 初始化 data_not3day 和data_threedays 两个list；判断是否3日上榜,不在字典中则为当日
        rid = self.__rid.split('_')[1]
        tf = {"7": True, "8": True, "10": True, "11": True,
              "28": True, "29": True}.get(rid, False)
        if tf:  # 如果为true表示三日的
            print("is_3days", self.stockcont["rid"], self.stockcont["name"])
            data_threedays.append(self.get_dict())
        else:
            # print("not_3days", self.stockcont["rid"], self.stockcont["name"])
            data_not3day.append(self.get_dict())
        pass

    def get_dict(self):
        return self.stockcont
        pass

    # __tr_xiwei()函数：提取传入的<tbody>下的五个<tr>,每次调用该函数会循环五次;返回保存五个席位的list,如下:
    # return [["华泰证券股份有限公司上海浦东新区福山路证券营业部", "5158.49", "89.30"], [同前面],[],[],[]]
    def __tr_xiwei(self, trs):
        # sub_data_gen=[tr('a').attr('title') for tr in trs]
        buy_sell = []
        for tr in trs:
            # print(tr.html()) #排查网页编码错误使用，勿删
            sub_data_dic = {"bs_name": 0, "buy_value": 0, "sell_value": 0}
            sub_data_dic["bs_name"] = tr("a").attr("title")
            sub_data_dic["buy_value"] = tr.children().eq(1).text()
            sub_data_dic["sell_value"] = tr.children().eq(2).text()
            chaE = tr.children().eq(3).text()  # 买入卖出的差额，只抓取、没有保存
            buy_sell.append(sub_data_dic)
        return buy_sell


class man_result(object):  # 用于计算均值和链接 数据库的类。
    """docstring for man_result"""

    # self.cnx =''
    # self.cursor =''
    def __init__(self):
        print('man_result类初始化。。。')

    def save_to_db_once(self, list_all):  # 这个写mysql的方法比上面的效率高
        add_data_to_db = (
            "INSERT INTO stocks (code, rid, name, reason, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out,date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s ,%s ,%s,%s  )")
        # add_data_to_db = ("INSERT INTO stocks1 (stock_code, rid, name, reason, totall_buy_in, totall_sell_out, buyer, buy_in, sell_out,date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s ,%s ,%s,%s  )")
        # print('·····························')
        for dic in list_all:
            for bs in dic["buyers"] + dic["sellers"]:
                data_data = (dic["stock_code"], dic["rid"], dic["name"], dic["reason"],
                             dic["totall_buy_in"], dic["totall_sell_out"], bs["bs_name"], bs["buy_value"],
                             bs["sell_value"], date_of_today)
                self.cursor.execute(add_data_to_db, data_data)
        self.cnx.commit()  # 循环外一次提交效率搞很多倍
        print("已经提交<龙虎榜详情数据>到数据库")

    def save_once(self, result):  # 这个写mysql的方法比上面的效率高
        add_data = (
            "INSERT INTO lhb_avg ( buy_all,buy_num,   sell_all,sell_num,buy_avg,sell_avg, date_in) VALUES (%s, %s, %s, %s, %s ,%s, %s )")
        # print('·····························')
        b_avg = round(result["buy_all"] / result["buy_num"], 2)
        s_avg = round(result["sell_all"] / result["sell_num"], 2)
        # print("买入大于1000万平均值：", b_avg, "卖出大于1000万平均值：", s_avg)
        data_data = (
            result["buy_all"], result["buy_num"], result["sell_all"], result["sell_num"], b_avg, s_avg, date_of_today)
        print("准备提交<上榜平均额>到数据库")
        self.cursor.execute(add_data, data_data)
        self.cnx.commit()  # 循环外一次提交效率搞很多倍

    def open_cnx(self):  # 存入MySQL数据库 mysql密码为root Cjf1991cjf!
        self.cnx = pymysql.connect(user='root', password='Cjf1991cjf!',
                                   host='127.0.0.1', database='tonghuashun', charset="utf8")
        self.cursor = self.cnx.cursor()
        pass

    def close_cnx(self):
        self.cursor.close()
        self.cnx.close()
        pass

    # buy_all=0;buy_num=0;sell_all=0;sell_num=0
    def map_arr(self, data_dic, res):
        # print(data_dic["buyers"])
        # print("卖方：",data_dic["sellers"])
        for bs in data_dic["buyers"] + data_dic["sellers"]:
            # print(bs)
            if float(bs["sell_value"]) > 1000:
                res["sell_all"] = res["sell_all"] + float(bs["sell_value"])
                res["sell_num"] = res["sell_num"] + 1
            if float(bs["buy_value"]) > 1000:
                res["buy_all"] = res["buy_all"] + float(bs["buy_value"])
                res["buy_num"] = res["buy_num"] + 1
            pass
        return res

    def xunhuan(self, datas):  # 循环数组统计非三天的大于1000万的额度，返回result字典
        res = {"buy_all": 0, "buy_num": 0, "sell_all": 0, "sell_num": 0}
        for data in datas:
            self.map_arr(data, res)
        pass
        res["buy_all"] = round(res["buy_all"], 2)
        res["sell_all"] = round(res["sell_all"], 2)
        return res


def getDate(i, j):
    year = '2017'
    mon = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    day = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
           '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    date_of_today = year + '-' + mon[i - 1] + '-' + day[j - 1]
    return date_of_today


# doc = pq(url='http://data.10jqka.com.cn/market/longhu/')
def start(this_date):
    global date_of_today
    date_of_today = this_date;  # getDate(12,12)
    URL = 'http://data.10jqka.com.cn/ifmarket/lhbggxq/report/' + date_of_today
    head = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0) ',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html, application/xhtml+xml, */*', 'Cookie': ''}
    r = requests.get(URL, headers=head)
    print('--------------------------')
    luanMa = re.compile(u'[\U00000000]')  # 以unicode的范围过滤乱码字符。不影响效率的情况下尽量把[00-1F]过滤掉，他们属于不可见字符；
    str_ok = luanMa.sub(u'', r.text)  # 也可以(u'[^\U00000020-\U0000007E]')：只保留可见字符；
    doc = pq(str_ok, parser='html')

    try:
        items = doc('.rightcol.fr')('.stockcont').items()
    except Exception as e:
        print('没有连网！！！')
    else:
        print('已连网抓到网页，继续进行！！！')
    # finally:
    #     print('继续进行！！！')
    # item('tbody')与item('tbody').items()有很大区别：需要使用for循环遍历时候用.items()；需要继续用pyquery选择器选择DOM时不加.items()
    # .items() 将pyquery对象格式化为python的对象【个人理解】
    stock = Info_unit()
    print(isinstance(items, Iterator));
    # print(next(items) is None)
    global count
    for item in items:  # 遍历每个个股
        # print(type(item),'-------==========')
        stock.jieXi(item)
        stock.is_3days()
        # data_not3day.append(stock.get_dict())
        count = count + 1
    if (count == 0):
        print('没有数据')
        return True
    return False


def print_info(start_time, result):
    end_time = datetime.now()
    print("插入数据库消耗时间：Cast: ", (end_time - start_time).microseconds / 1000, "ms")
    print('Done！！！')
    print('--------------------------------------------------')
    print("今日总共上榜股票个数：", count)
    print('当日上榜数量：', len(data_not3day), ' 三日上榜数量：', len(data_threedays))
    print(result)
    print('买入平均值：', round(result['buy_all'] / result['buy_num'], 2), '万元 ，卖出平均值：',
          round(result['sell_all'] / result['sell_num'], 2), '万元 ')
    # print('=============================================================')


mouth = 1;
tian = 1;
date_week = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
fileout = open('logs.txt', 'a', encoding="utf-8")
fileout.write('=====================================================================\n')
fileout.write('本轮日志记录开始时间：' + datetime.now().strftime("%Y-%m-%d-->%H:%M:%S ") + '\n')
while tian < 32:  # 循环一年
    # global data_threedays;data_not3day;count
    data_threedays = []  # 保存三日龙虎榜的list
    data_not3day = [];
    count = 0
    print('=============================================================')
    start_time = datetime.now()
    riqi = getDate(mouth, tian)
    try:
        week = datetime.strptime(riqi, "%Y-%m-%d").weekday()
        print(riqi, date_week[week], ' 的数据：')
        nodata = start(riqi)
        if nodata:
            # write_log();没有数据的日期写入txt日志
            fileout.write("······日期： " + str(riqi) + " " + date_week[week] + " 没有数据...\n")
            continue;
        getresult = man_result()
        # print('------------',data_not3day)
        print('·····························')
        result = getresult.xunhuan(data_not3day)  # 计算平均值
        getresult.open_cnx()
        getresult.save_once(result)  # 写入数据库：上榜平均额
        getresult.save_to_db_once(data_not3day + data_threedays)  # 写入数据库：上榜详情
        getresult.close_cnx()
        print('·····························')
        print_info(start_time, result)
        fileout.write("······日期： " + str(riqi) + " " + date_week[week] + " 数量：" + str(count) + "  消耗时间：Cast: " + str(
            (datetime.now() - start_time).microseconds / 1000) + "ms \n")
        pass
    except Exception as e:
        print('--------------------------')
        print('while循环中报错了！！！出错日期： ', riqi)
        print("错误类型：", repr(e))
        traceback.print_exc()
        # print(logging.exception(e))
        fileout.write('-------------------------------------------\n')
        fileout.write('错误堆栈 &&' + '出错日期： ' + riqi + '\n')
        fileout.write(traceback.format_exc() + '\n')
        fileout.flush()  # 前面可能会写文件出错导致退出程序无法正常close()文件，导致日志无法持久化到磁盘。这里强刷一下
    else:
        pass
    finally:
        tian += 1
        if tian == 32 and mouth < 12:
            print('下一月开始')
            mouth += 1;
            tian = 1
            pass
    pass
print("循环完成！！！")
fileout.write('本轮日志记录结束时间：' + datetime.now().strftime("%Y-%m-%d-->%H:%M:%S ") + '\n')
fileout.close()
