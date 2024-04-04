import socket
import json
import emailproc


emailor = None

class Protocol:
    TYPE_HELLO            = 0
    TYPE_ADD_USER_REQUEST = 1
    TYPE_RESPONSE         = 4

    STATUS_SUCCESS = 0
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

    
class NetWorkProc:
    def __init__(self,addr,rcvbuflen):
        self.protocol = Protocol()
        self.addr = addr

        self.rcvbuflen = rcvbuflen
    
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # ("0.0.0.0",33333)
        self.udpsock.bind(self.addr)

    def rcv_data_block(self):
        data, address = self.udpsock.recvfrom(self.rcvbuflen)

        return json.loads(data.decode()),address
    
    def hello_msg_procs(self,rec_data,address):
        self.udpsock.sendto(self.protocol.hello_msg().encode("utf-8"),address)

    def add_user_msg_proc(self,rec_data,address):
        global emailor
        self.udpsock.sendto(self.protocol.add_user_response_msg(rec_data["username"],self.protocol.STATUS_SUCCESS).encode("utf-8"),address)
        # 添加用户到userinfo数据库中

        # 发送邮件
        emailor.send_add_user_email(rec_data["email"],rec_data["username"])
    
    def dispatch(self):
        rec_data , address = self.rcv_data_block()
        if rec_data['type'] == self.protocol.TYPE_HELLO:
            self.hello_msg_procs(rec_data , address)
        elif rec_data['type'] == self.protocol.TYPE_ADD_USER_REQUEST:
            self.add_user_msg_proc(rec_data , address)
    


if __name__ == "__main__":
    print("start lexilab server...")
    emailor = emailproc.EamilProc("1747106747@qq.com","smwnhiwpcdcufege")
    netproc = NetWorkProc(("0.0.0.0",33333),4096)
    while True:
        netproc.dispatch()

    emailor.exit()


        

        

