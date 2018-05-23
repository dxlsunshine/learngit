import time
def timing(func):
	def wrapper(*args,**kargs):
		time.clock()
		func(*args,**kargs)
		t = time.clock()
		print('用时%05.2f秒' %t)
	return wrapper