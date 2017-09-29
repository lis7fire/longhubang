import os,sys
from multiprocessing import Process
import socket,threading

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

def send_meg(mesg,con):
	con.send(mesg.encode('utf-8'))
	pass
def get_meg(length,con):
	return con.recv(length).decode('utf-8')
	pass
def exitus(ser,data,con):
	send_meg('你关闭连接了！',con)
	send_meg('exit',con)
	print('用户',addr[1],'主动关闭了连接。。。')
	print('-----------------------------------------')
	con.close()
	if data=='exitall':
		ser.close()
		return True
	return False
def p_con(ser,con,addr):
	print('子进程开始运行')
	try:
		send_meg('你好，欢迎加入！',con)
		send_meg('下面开始通信...',con)
		while True:
			data=get_meg(1024,con)
			print('客户端ip：',addr,'收到的消息：',data)
			if data=='ls':
				send_meg(str(len(threading.enumerate())-1),con)
			if data=='exit' or data=='exitall':
				exitus(ser,data,con)
				break
			else:
				strs='你好，'+data
				send_meg(strs,con)
	except Exception as e:
		con.close()
		ser.close()
		print('出错了')
		raise e
	pass

ser=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ser.bind(('0.0.0.0',8010))
ser.listen(9)
print('服务器正在监听.....')
print('开始监听连接...')
while True:
	con,addr=ser.accept()
	print('启动新进程...')
	p_connect=threading.Thread(target=p_con,args=(ser,con,addr))
	# p_connect=Process(target=p_con,args=(con,addr)) //多进程无法共享资源，所以会提示socket被重复使用，因为ser参数无法共享传递
	p_connect.start()
	print('---------------------------------------新用户加入了：', os.getpid(),threading.current_thread().name)
	print()
	# p_connect.join()
	# ser.getsockopt()
	# if exitus(ser,data,con):break
	
print('服务器已关闭！！！')

