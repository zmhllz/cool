import random
from threading import Thread, current_thread

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



