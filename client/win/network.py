from PyQt5.QtCore import QThread

class NetworkClass(QThread):
    def __init__(self):
        super(NetworkClass,self).__init__()

        self.working = True

    def run(self):
        while( self.working == True ):
            self.sleep(2)
            print("in network thread")

    def exit(self):
        print("exit")
        self.working = False
        self.wait()


