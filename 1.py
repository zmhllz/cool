import random
from threading import Thread, current_thread
from threading import Thread, current_thread

def target01(args1, args2):
	print("这里是{}".format(current_thread().name))

# 创建线程
thread01 = Thread(target=target01, args="参数", name="线程1")
# 设置守护线程【可选】
thread01.setDaemon(True)
# 启动线程
thread01.start() 

def create_a_phone():
    # 第二位数字
    for o in range(100):
        second = [3, 4, 5, 7, 8][random.randint(0, 4)]
        # 第三位数字
        third = {3: random.randint(0, 9),
                4: [5, 7, 9][random.randint(0, 2)],
                5: [i for i in range(10) if i != 4][random.randint(0, 8)],
                7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
                8: random.randint(0, 9), }[second]
        suffix = random.randint(10000000, 99999999)
        phone = "1{}{}{}".format(second, third, suffix)
        print(phone)
        


create_a_phone = Thread(target=create_a_phone, daemon=True)

# create_a_phone.setDaemon(True)
create_a_phone.start() 



