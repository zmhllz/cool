from threading import Thread, current_thread

def target01(args1, args2):
	print("这里是{}".format(current_thread().name))

# 创建线程
thread01 = Thread(target=target01, args="参数", name="线程1")
# 设置守护线程【可选】
thread01.setDaemon(True)
# 启动线程
thread01.start() 
