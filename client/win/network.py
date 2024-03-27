from PyQt5.QtCore import QThread
import json
import socket
# Queue模块中提供了同步的、线程安全的队列类
from queue import Queue

class Protocol:
    TYPE_HELLO = 0

    def __init__(self):
        pass

    def hello_msg(self) -> str:
        msg = {
            "type": self.TYPE_HELLO
        }

        return json.dumps(msg,ensure_ascii=False)



class NetworkClass(QThread):
    def __init__(self,port,serverip,serverport,timeout = 2):
        super(NetworkClass,self).__init__()

        self.working = True

        self.udpsock    = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port       = port
        self.serverip   = serverip
        self.serverport = serverport
        self.buflen     = 4096
        # self.udpsock.bind(("0.0.0.0",self.port))

        # 任务队列
        self.taskQueue = Queue()

        self.protocol = Protocol()
        # 设置为非阻塞模式，并设置超时时间
        # self.udpsock.setblocking(False)
        self.udpsock.settimeout(timeout)
    
    def add_task(self,task):
        self.taskQueue.put(task)

    def run(self):
        while( self.working == True ):
            if self.working:
                if self.say_hello():
                    if not self.taskQueue.empty():
                        print("有任务需要执行")
                    else:
                        print("没有任务执行")
                        self.sleep(3)
            else:
                if not self.taskQueue.empty():
                    # 需要保存任务
                    pass

    def say_hello(self):
        self.udpsock.sendto(self.protocol.hello_msg().encode('utf-8'), (self.serverip, self.serverport))
        count = 0
        while( count <3 ):
            try:
                data, server = self.udpsock.recvfrom(self.buflen)
                if json.loads(data.decode())['type'] == self.protocol.TYPE_HELLO and server[0] == self.serverip:
                    return True
            except:
                count += 1
        return False


    def exit(self):
        self.working = False
        self.wait()


