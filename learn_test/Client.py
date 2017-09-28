import os,sys
from multiprocessing import Process
import socket

class clients(object):
	"""docstring for clients"""
	def __init__(self, ip_port):
		self.csock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# self.csock.connect(ip_port)


c=clients(('127.0.0.1',8001))
c.csock.connect(('127.0.0.1',8003))
c.csock.send(b'Luckyv')
print((c.csock.recv(1024)).decode('utf-8'))
c.csock.close()