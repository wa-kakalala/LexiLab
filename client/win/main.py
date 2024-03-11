from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtGui  import QMouseEvent,QIcon
import loginpage 
import mainpage
from sqlproc import SqlProc
import sys

class LoginWindow (QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False
    def __init__(self):
        super().__init__()
        self.ui = loginpage.Ui_LoginWindow()
        self.ui.setupUi(self)

        self.ui.login_btn.clicked.connect(self.select_login_page_proc)
        self.ui.register_btn.clicked.connect(self.select_register_page_proc)

        self.ui.login_confirm_btn.clicked.connect(self.login_confirm_proc)

        self.ui.register_confirm_btn.clicked.connect(self.register_confirm_proc)

        self.ui.login_info.setText("")
        self.ui.register_info.setText("")
        self.select_login_page_proc()
        self.show()

    def select_login_page_proc(self):
        self.ui.register_page.hide()
        self.ui.login_page.show()

    def select_register_page_proc(self):
        self.ui.login_page.hide()
        self.ui.register_page.show()

    def register_confirm_proc(self):
        print(self.ui.register_username_input.text())
        print(self.ui.register_pwd_input.text())
        print(self.ui.register_pwd_input_confirm.text())

    ############### 重写移动事件 Begin ################
    def mouseMoveEvent(self, e: QMouseEvent):  
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
    ############### 重写移动事件  End  ################

    def login_confirm_proc(self):
        if( self.ui.username_input.text() == "yyrwkk" and self.ui.password_input.text() == "1234"):
            self.close()
            self.win = MainWindow()
        else:
            print("UserName is not match with PassWord !")


class MainWindow (QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False
    def __init__(self):
        super().__init__()

        self.sqlor = SqlProc("./db/test.db","test")

        self.ui = mainpage.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.logout.clicked.connect(self.logout_btn_proc)
        self.ui.commit_btn.clicked.connect(self.commit_btn_proc)
        self.show()

    ############### 重写移动事件 Begin ################
    def mouseMoveEvent(self, e: QMouseEvent):  
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
    ############### 重写移动事件  End  ################
            
    def logout_btn_proc(self):
        self.close()
        self.win = LoginWindow()
        self.sqlor.exit()

    def commit_btn_proc(self):
        print(self.ui.term_input.toPlainText())
        print(self.ui.explain_input.toPlainText())
        self.sqlor.insert(["term","explain" ],[self.ui.term_input.toPlainText(),self.ui.explain_input.toPlainText()])
        
        print("commit")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    sys.exit(app.exec_())
