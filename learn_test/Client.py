import os,sys
from multiprocessing import Process
import socket

class clients(object):
	"""docstring for clients"""
	def __init__(self, ip_port):
		self.csock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.csock.connect(ip_port)
	def send_meg(self,meg):
		return self.csock.send(meg.encode('utf-8'))
		pass
	def get_meg(self):
		return self.csock.recv(1024).decode('utf-8')
		pass

c=clients(('127.0.0.1',8010))
c.send_meg('奥特曼')
print('收到的消息：',c.get_meg())
while True:
	try:
		info=c.get_meg()
		print('收到的消息：',info)
		c.send_meg(input('请输入：'))
		if info=='你好，exit':
			c.csock.close()
			print('连接已断开！')
			break
			pass
	except Exception as e:
		c.csock.close()
		raise e
print('远程服务器关闭了！')
