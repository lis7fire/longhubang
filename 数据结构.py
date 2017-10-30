#!/usr/bin/env python3
#coding: utf-8
# 上面两句注释必须要，防止无法打印中文的

import datetime
import os,sys
from pyquery import PyQuery as pq
from multiprocessing import Process
import pymysql.cursors

date_of_today = datetime.datetime.now().strftime("%Y-%m-%d")
#os.mknod(date_of_today)
#date_of_today='2017-05-11'

def write_mou(pro_name):
	print('进程 ',pro_name,'启动，进程号为：',os.getpid())
	print('进程 ',pro_name,'启动，他的父进程号为：',os.getppid())
	pass
def read_mou():
	pass
if __name__ == '__main__':
	p=Process(target=write_mou,args=('zi',))
	print('本进程 启动111，进程号为：',os.getpid())
	print('子进程即将启动。。。')
	p.start()
	p.join()
	print('子进程end')

print('本进程 ',__name__,'启动进程号为：',os.getpid())
print('Done！！！' )

class Solution(object):
	"""docstring for Solution"""
	def Find(self, target,array):
		print(len(array))
		hang_num=len(array)
		lie_num=len(array[0])
		i=hang_num-1
		j=0
		while i>=0 and j<lie_num:
			if target==array[i][j]:
				return "true"
			elif target>array[i][j]:
				j+=1
			else :
				i-=1
			pass
		return "false"
			
a=Solution()
b=[x for x in range(1,5)] 
c=[]
n=6;i=0
for x in range(1,n+1):
	c.append([x+i for x in range(1,n+1)] )
	i+=1
print(b)
c=[[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]]
print(c)
print(a.Find(5,c))
#第二题：请实现一个函数，将一个字符串中的空格替换成“%20”。例如，当字符串为We Are Happy.则经过替换之后的字符串为We%20Are%20Happy。
class Solution:
	# s 源字符串
	def replaceSpace(self, s):
		print(s)
		tem=''
		# for x in s:
		#	 print(tem)
		#	 if x==' ':
		#		 x='%20'
		#	 tem+=x
		tem=s.replace(" ",'%20')
		print(tem)
s='We Are Happy'
Solution().replaceSpace(s)

#第三题：输入一个链表，从尾到头打印链表每个节点的值。
class ListNode:
	__slots__=['val','next']	#限定Node实例的属性
	def __init__(self, x):
		self.val = x
		self.next = None
	def getval(self):
		return self.val
	def getnext(self):
		return self.next
	def setval(self,val):
		self.val=val
	def setnext(self,next):
		self.next=next

class Solution:
	# 返回从尾部到头部的列表值序列，例如[1,2,3]
	def printListFromTailToHead(self, listNode):
		# write code here
		ls=list(listNode)
		res=[] 
		for x in ls:
			res.insert(0,x)
		i=len(res);print(res)
		return res
	def tess(self, listNode):
		result = []
		if listNode is None:
			return result
		while listNode.next is not None:
			result.extend([listNode.val])
			listNode=listNode.next
		result.extend([listNode.val])
		return result[::-1]

l1=ListNode(1)
l2=ListNode(2)
l3=ListNode(3)
print(type(l2))
c=set([67,0,24,58])
print(c)
print(Solution().printListFromTailToHead([67,0,24,58]))

#第四题：输入某二叉树的前序遍历和中序遍历的结果，请重建出该二叉树。假设输入的前序遍历和中序遍历的结果中都不含重复的数字。例如输入前序遍历序列{1,2,4,7,3,5,6,8}和中序遍历序列{4,7,2,1,5,3,8,6}，则重建二叉树并返回。
print([0, 1, 2, 3, 4, 5, 6, 7, 8, 9][::2])
class TreeNode:
	def __init__(self, x):
		self.val = x
		self.left = None
		self.right = None
class Solution:
	# 返回构造的TreeNode根节点
	def bian_tin(self,tar,tin,ls_r):
		i=0
		# print(tar,i,tin)
		while tar!=tin[i] and i<len(tin):
			i+=1
		return tin[:i],tin[i+1:]
	def reConstructBinaryTree(self, pre, tin):
		# write code here
		ls_left=tin;ls_r=tin
		res=[];i=0
		tem=tin
		while i<len(pre):
			print(i,'len',ls_left)
			ls_left,ls_r=self.bian_tin(pre[i],ls_left,ls_r)
			i+=1
			if ls_left !=[]:
				res.append(pre[i])
				print('rootwei',pre[i])
			else:
				print('左树完成')
		return  res

# print(Solution().reConstructBinaryTree([1,2,4,7,3,5,6,8],[4,7,2,1,5,3,8,6]))

class Listchain(object): #自己实现的单链表
	"""docstring for Listchain"""
	__slots__=['size','head']   #限定实例的属性
	def __init__(self):
		self.size=0
		self.head = ListNode(self.size)
	def get_size(self):
		print(self.size)
	def add_last(self,node):#在尾部插入结点
		last=ListNode(None)
		tem_head=ListNode(None)
		tem_head=self.head #移动指针		
		if self.head.next == None:#空链表
			self.head.next=node
		else:
			# last=bianli(self.size)
			while tem_head.next != None:
				tem_head=tem_head.next
		tem_head.next=node
		self.size+=1
		self.head.val=self.size
		print('增加第i个',node.val)

	def del_i(self,i):
		tem_head=ListNode(None)
		tem_head=self.head #移动指针
		if(i>self.size):
			print('参数越界')
			return
		x=1;print('---------------------')
		while x<i: #移动i次来找到结点i
			tem_head=tem_head.next
			x+=1
			pass
		print('删除之前的值',tem_head.val)
		tem_head.next=tem_head.next.next
		self.size-=1
		self.head.val=self.size
		print('删除第',i,'个结点',tem_head.next.val)
		pass

	def bianli(self):#遍历查找第i个节点 ,i
		tem_head=ListNode(0)
		tem_head=self.head
		allof=[]
		while tem_head.next != None:
			allof.append(tem_head.val)
			tem_head=tem_head.next
			pass
		allof.append(tem_head.val);print('---------------------')
		print('链表长度',allof[0])
		print('遍历打印所有结点',allof[1:]);print('---------------------')
		return tem_head
		pass
print('======================================')
A=Listchain()
A.add_last(ListNode(2))
A.add_last(ListNode(57))
A.add_last(ListNode(1))
A.add_last(ListNode(9))
A.add_last(ListNode(100))
A.bianli()
A.del_i(8)
A.bianli()
