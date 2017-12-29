#!/usr/bin/python3
# coding: utf-8
# 上面两句注释必须要，防止无法打印中文的

from datetime import datetime, date
import os
import re
from pyquery import PyQuery as pq
import pymysql.cursors
import requests
# import urllib,urllib2,re,json

ids=[]
names=[]
personids=[]
filein=open('luanma.txt','r')
print('开始读取in文件：')
while 1:
	temp=filein.readline()
	if temp:
		# print(temp.strip())
		if temp.find("GDZQGFYXGSNBBLX")!= -1:
			print( '······'+str(temp.find("GDZQGFYXGSNBBLX"))+temp)
	else:
		break;
filein.close()

print( ids)
print(names)
print(personids)

fileout=open('luanma.txt','a',encoding="gbk");
# fileout.write(ids[x].encode('utf-8').strip().lstrip()+',')
# fileout.write(names[x].encode('utf-8').strip().lstrip()+',')
fileout.write("hahd大是大非"+'\n')

# print fileout.read(1)
pass
date_of_today='2014-12-29'#items = doc('')

URL = 'http://data.10jqka.com.cn/ifmarket/lhbggxq/report/'+date_of_today
head = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0) ',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html, application/xhtml+xml, */*', 'Cookie': ''}
r = requests.get(URL, headers=head)
print('--------------------')
# print("响应头", r.headers)
# print("请求头", r.request.headers)
# print(r.text,"utf-8")
# fileout.write(r.text+'\n')
fileout.close()
if r.text.find("GDZQGFYXGSNBBLX")!= -1:
	print(r.text.find("GDZQGFYXGSNBBLX"))
	print( '······'+r.text[150090:150112])  # 一字节一字节的测试，看乱码字符占几位，知道占几位之后再去按照unicode编码范围过滤。
											#汉字占两位，所以占一位的不可能是汉字，过滤时可以保留汉字。
luanMa=re.compile(u'[^\U00000000-\U0000001F]') #不影响效率的情况下尽量把00-1F过滤掉，属于不可见字符；
tt=luanMa.sub(u'',r.text)
print("打印乱码字符： \n",tt.strip())
print('----------------------\n  <a href="http://data.10jqka.com.cn/market/lhbyyb/orgcode/GDZQGFYXGSNBBLX		ZQYYB/"   \
 target="_blank" class="details" title="光大证券股份有限公司宁波北仑新碶证券营业部">光大证券股份有限公司宁波北仑新碶证券营业部</a>')

print('本次日志记录时间：'+datetime.now().strftime("%Y-%m-%d-->%H:%M:%S ")+'\n')

print('--------------下面是读写二进制文件:----------------------------')
#下面是读写二进制文件，以图片为例：多次读写对比图像的内容，可以感知图片底层的二进制展现。
start_time=datetime.now()
bfile=open("./a.jpg",'rb')
print('------')
a=b''
while bfile.readable():
	tmp=bfile.read()
	a+=tmp
	if not tmp:
		break;
print(type(a))
print(len(a))
print(chr(a[len(a)-1]),a[-7],a[-1]) # 打印ASCII码，结果以十进制表示。a是bytes类型，但a[-1]是int类型；，

wbfile=open("./b.jpg","wb")
wbfile.write(a[0:9697])
wbfile.write(b'abcd') # 只要不是在文件头 修改 比特数据，在其余任何地方增删改比特位都不影响图片的格式损坏，里面图像会失真，但是能够打开。
wbfile.write(a[3197:41976])
wbfile.write(b'0abcde!')
# wbfile.flush()
bfile.close();
wbfile.close()
print("任务消耗时间：Cast: ", (datetime.now() - start_time).microseconds / 1000, "ms")
print('OK!!!')
