import os,sys
from multiprocessing import Process
import socket

class server(object):
	"""docstring for server"""
	def __init__(self, arg):
		self.ser=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.ser.bind(('0.0.0.0',8000))
		self.ser.listen(9)
		print('Waiting for connecting.........')

# s=server('服务器')
ser=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ser.bind(('0.0.0.0',8003))
ser.listen(9)
while True:
	print('开始监听链接。。。')
	sock,addr=ser.accept()
	data=sock.recv(1024)
	print('客户端ip：',addr,' 你好，',data)
	send_meg='我是服务器127'+data.decode('utf-8')
	sock.send(send_meg.encode('utf-8'))
	sock.send('hhhhhhh'.encode('utf-8'))
	sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
	sock.close()
	pass
