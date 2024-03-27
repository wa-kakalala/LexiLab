import socket
import json

class Protocol:
    TYPE_HELLO = 0

    def __init__(self):
        pass

    def hello_msg(self) -> str:
        msg = {
            "type": self.TYPE_HELLO
        }

        return json.dumps(msg,ensure_ascii=False)


protocol = Protocol()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 44444))
while True:
    data, address = sock.recvfrom(4096)
    if json.loads(data.decode())['type'] == protocol.TYPE_HELLO:
        sock.sendto(protocol.hello_msg().encode("utf-8"),address)

