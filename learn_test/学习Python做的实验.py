#!/usr/bin/env python3
#-*-coding:utf-8-*- 
# 上面两句注释必须要，防止无法打印中文的
from __future__ import print_function
import sys
from functools import reduce
import logging
import os

print(os.environ)
try:
	print('ttt')
	r=10/3
	print(r)
except BaseException as e:
	print('有错误：')
	print(e)
else:
	print('没有错误执行ELSE!!!')
finally:
	r=10/10
	print(r)
print('END')

logging.info('-------------- = %d' % 100)

# print(sys.path)
while True:
	print('-----计算涨幅工具-----')
	openpr=float(input("输入开盘价："))
	clo=float(input("输入收盘价："))
	cha=(clo-openpr)*100/openpr
	print("涨幅为：%.2f%%" % cha)
	pass

a=3
b='MySQL'
print('hello,')
print(b[1:])
print(b[0:2]+'lucky')
print(b[2:]*3)
print('打印中%d文%.2f ff' % (12,34.567));print(a)
list3=['name',20,'school']
print(list3[0:2])
list3.append("aaa")
list3[1]=100
print(17.5*253)
print (list3)
b=[12,'43']
print('www',b)
L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
]
print(L[1][1])

def triangles():
	lists=[]
	lista=[x for x in [1,2]]
	print('#',lista)
	return lists
	pass
	

start=1
sec=[1,1]
triangles()
s=[x*x for x in range(5)]
print(s)
def ad(x,y):
	# print(y)
	return x
	pass
aaa=reduce(ad,['1', 'r', 'e', 'a', '5'])

def char2num(s):
	return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

aaa= map(char2num, '13579')
inp=['adam', 'LISA', 'barT']
def zhuanhuan(leter):
	first=leter[0].upper()
	aftr=leter[1:].lower()
	print('附一个：',first,'  第二个：',aftr)
	return first+aftr
	pass
L2=list(map(zhuanhuan, inp))
print(L2)

L1=[3, 3, 3]
def prod(L):
	def pl(x,y):
		return x*y
		pass
	return reduce(pl,L)
aa=prod(L1)
print(aa)

# 下面是将字符串格式化为小数
point=0
def str2float(s):
	L1=[x for x in s]
	result=reduce(red,map(mmap,L1))
	print(result)
	return result
	pass
def mmap(s):
	return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '.': -1}[s]
def red(x,y):
	global point
	if y==-1:
		point=1
		print('x=',x,'y=',y)
		return x  #reduce中的return表示结束本轮计算，开始下一个元素的计算
	elif point==0:
		return x*10+y
	else :
		print('p=',point)
		point=point*10
		return x+y/point
str='12.3323'
str2float(str)
