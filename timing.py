from queue import Queue, Empty
from threading import Thread, Timer


class EventManager:
    """
    事件管理器
    """

    def __init__(self):
        """初始化事件管理器"""
        # 事件对象列表
        self.__eventQueue = Queue()
        # 事件管理器开关
        self.__active = False
        # 事件处理线程
        self.__thread = Thread(target=self.__Run)
        self.count = 0
        # 这里的__handlers是一个字典，用来保存对应的事件的响应函数
        # 其中每个键对应的值是一个列表，列表中保存了对该事件监听的响应函数，一对多
        self.__handlers = {}

    def __Run(self):
        """引擎运行"""
        print('{}_run'.format(self.count))
        while self.__active:
            try:
                # 获取事件的阻塞时间设为1秒:如果在1s内队列中有元素，则取出；否则过1s之后报Empty异常
                print("\n  <__RUN::>开始get:", self.__eventQueue)
                event = self.__eventQueue.get(block=True, timeout=1)
                print("  <__RUN::>取到事件了：", event)
                self.__EventProcess(event)
            except Empty:
                print("  <__RUN::>队列是空的")
                pass
            self.count += 1
            print("  <__RUN::>Run中的count:", self.count)

    def __EventProcess(self, event):
        """处理事件"""
        print('{}_EventProcess'.format(self.count))
        # 检查是否存在对该事件进行监听的处理函数
        if event.type_ in self.__handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            for handler in self.__handlers[event.type_]:
                # 这里的handler就是放进去的监听函数，这里会跳转到listener.ReadArticle(event)
                handler(event)
        self.count += 1

    def Start(self):
        """启动"""
        print('{}_Start'.format(self.count))
        # 将事件管理器设为启动
        self.__active = True
        # 启动事件处理线程
        self.__thread.start()
        self.count += 1
        print("start中的count:", self.count)

    def Stop(self):
        """停止"""
        print('{}_Stop'.format(self.count))
        # 将事件管理器设为停止
        self.__active = False
        # 等待事件处理线程退出
        self.__thread.join()
        self.count += 1

    def AddEventListener(self, type_, handler):
        """绑定事件和监听器处理函数"""
        print('{}_AddEventListener'.format(self.count))
        # 尝试获取该事件类型对应的处理函数列表，若无则创建
        try:
            handlerList = self.__handlers[type_]
        except KeyError:
            handlerList = []
            self.__handlers[type_] = handlerList
        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)
        print(self.__handlers)
        self.count += 1

    def RemoveEventListener(self, type_, handler):
        """移除监听器的处理函数"""
        print('{}_RemoveEventListener'.format(self.count))
        try:
            handlerList = self.__handlers[type_]
            # 如果该函数存在于列表中，则移除
            if handler in handlerList:
                handlerList.remove(handler)
            # 如果函数列表为空，则从引擎中移除该事件类型
            if not handlerList:
                del self.__handlers[type_]
        except KeyError:
            pass
        self.count += 1

    def SendEvent(self, event):
        """发送事件，向事件队列中存入事件"""
        print('{}_SendEvent'.format(self.count))
        self.__eventQueue.put(event)
        self.count += 1


class Event:
    """事件对象"""
    def __init__(self, type_=None):
        print("实例化事件对象：事件类型：{},事件：self.dict".format(type_))
        # 事件类型
        self.type_ = type_
        # 字典用于保存具体的事件数据
        self.dict = {}

# ============================  测试  ==================================


# 事件名称  新文章
EVENT_ARTICLE = "Event_Article"


class PublicAccounts:
    """
    事件源 公众号
    """
    def __init__(self, eventManager):
        print("实例化公众号")
        self.__eventManager = eventManager

    def WriteAndSendNewArtical(self):
        """
        事件对象：写了并推送了新文章
        """
        event = Event(type_=EVENT_ARTICLE)
        event.dict["article"] = '《文章名：第一百零八回》'

        # 发送事件
        print(u'公众号推送新文章\n')
        self.__eventManager.SendEvent(event)


class Listener:
    """
    监听器 订阅者
    """
    def __init__(self, username):
        self.__username = username

    # 监听器的处理函数 读文章
    def ReadArtical(self, event):
        print(u'%s 收到新文章' % self.__username)
        print(u'正在阅读新文章内容：%s' % event.dict["article"])


def test():
    """
    测试函数
    """
    # 1.实例化『监听器』
    listener1 = Listener("小明")  # 订阅者1
    listener2 = Listener("小红")  # 订阅者2

    # 2.实例化『事件管理器』
    eventManager = EventManager()

    # 3.绑定『事件』和『监听器响应函数』
    eventManager.AddEventListener(EVENT_ARTICLE, listener1.ReadArtical)
    eventManager.AddEventListener(EVENT_ARTICLE, listener2.ReadArtical)

    # 4.启动『事件管理器』
    #   注意：4.1 这里会启动一个新的事件处理线程，一直监听下去,可以看__run()中while循环；
    #        4.2.同时主线程会继续执行下去
    eventManager.Start()

    # 5.实例化『事件源』
    publicAcc = PublicAccounts(eventManager)

    # 6.定时启动『事件源』中的『生成事件对象以及发送事件』
    timer = Timer(5, publicAcc.WriteAndSendNewArtical)
    timer.start()


if __name__ == '__main__':
    test()

