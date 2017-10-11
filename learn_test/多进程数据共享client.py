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

print('Client')
c=clients(('127.0.0.1',8000))
while True:
	try:
		info=c.get_meg()
		print('收到的消息：',info)
	except Exception as e:
		c.csock.close()
		raise e
print('远程服务器关闭了！')
