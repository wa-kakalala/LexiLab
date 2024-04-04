from PyQt5.QtCore import QThread
import json
import socket
# Queue模块中提供了同步的、线程安全的队列类
from queue import Queue

class Protocol:
    TYPE_HELLO            = 0
    TYPE_ADD_USER_REQUEST = 1
    TYPE_RESPONSE         = 4
    def __init__(self):
        pass

    def hello_msg(self) -> str:
        msg = {
            "type": self.TYPE_HELLO
        }

        return json.dumps(msg,ensure_ascii=False)
    
    def add_user_response_msg(self,username,status):
        msg = {
            "type": self.TYPE_RESPONSE,
            "username": username,
            "status": status
        }
        return json.dumps(msg,ensure_ascii=False)

class NetworkClass(QThread):
    def __init__(self,serverip,serverport,timeout = 2):
        super(NetworkClass,self).__init__()

        self.working = True

        self.udpsock    = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.port       = port
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
        # task 基本格式
        # {
        #   "type": xxx ,
        #   "content": xxx
        # }

    def do_task(self):
        task = self.taskQueue.get()
        if task["type"] == self.protocol.TYPE_ADD_USER_REQUEST :
            if not self.add_user_request(task["content"]):
                # 执行任务失败了
                self.taskQueue.put(task)
            # else:
                # print("send add user request successfully")


    def run(self):
        while( self.working == True ):
            if self.working:
                if self.say_hello():
                    if not self.taskQueue.empty():
                        # print("有任务需要执行")
                        self.do_task()
                    else:
                        # print("没有任务执行")
                        self.sleep(60)
                        
                else:
                    self.sleep(2*60)
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
    
    def add_user_request(self,content:str):
        raw_data = json.loads(content)
        self.udpsock.sendto(content.encode('utf-8'), (self.serverip, self.serverport))
        count = 0
        while( count <3 ):
            try:
                data, server = self.udpsock.recvfrom(self.buflen)
                res_data = json.loads(data.decode())
                if res_data['type'] == self.protocol.TYPE_RESPONSE and res_data["status"] == 0 and res_data["username"] == raw_data["username"]:
                    return True
            except:
                count += 1
        return False


    def exit(self):
        self.working = False
        self.wait()


