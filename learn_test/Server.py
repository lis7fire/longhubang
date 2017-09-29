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
	def send_meg(self,mesg):
		self.ser.send(mesg.encode('utf-8'))
		pass
	def get_data(self):
		pass
	def get_ser(self):
		return self.ser
		pass
def send_meg(mesg,sock):
	sock.send(mesg.encode('utf-8'))
	pass
def get_meg(length,sock):
	return sock.recv(length).decode('utf-8')
	pass
def exitus(data,sock):
	send_meg('你关闭连接了！',sock)
	send_meg('exit',sock)	
	sock.close()
	if data=='exitall':
		ser.close()
		return True
	return False

ser=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ser.bind(('0.0.0.0',8002))
ser.listen(9)
print('服务器正在监听.....')
print('开始监听连接...')
sock,addr=ser.accept()
while True:
	try:
		data=get_meg(1024,sock)
		print('客户端ip：',addr,'收到的消息：',data)
		strs='你好，'+data
		send_meg(strs,sock)
		if data=='exit' or data=='exitall':
			# if exitus(data,sock):break
			break
	except Exception as e:
		sock.close()
		ser.close()	
		raise e
print('服务器已关闭！！！')

