from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtGui  import QMouseEvent,QIcon
import loginpage 
import mainpage
from sqlproc import SQLClass
import sys
import hashlib
import re
import datetime

global_username = ''
global_password = ''
global_remember = False

class LoginWindow (QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False
    userinfo_db = None
    def __init__(self,userinfo_db,lexilab_db):
        global global_username,global_password,global_remember
        super().__init__()
        self.userinfo_db = userinfo_db
        self.lexilab_db  = lexilab_db
        self.ui = loginpage.Ui_LoginWindow()
        self.ui.setupUi(self)

        self.ui.login_btn.clicked.connect(self.select_login_page_proc)
        self.ui.register_btn.clicked.connect(self.select_register_page_proc)

        self.ui.login_confirm_btn.clicked.connect(self.login_confirm_proc)

        self.ui.register_confirm_btn.clicked.connect(self.register_confirm_proc)

        self.ui.username_input.setText(global_username)
        self.ui.password_input.setText(global_password)

        self.ui.remember_box.setChecked(global_remember)

        self.ui.login_info.setText("")
        self.ui.register_info.setText("")
        self.select_login_page_proc()
        self.show()

    def select_login_page_proc(self):
        self.ui.login_info.setText("")
        self.ui.register_info.setText("")
        self.ui.register_page.hide()
        self.ui.login_page.show()

    def select_register_page_proc(self):
        self.ui.login_info.setText("")
        self.ui.register_info.setText("")
        self.ui.login_page.hide()
        self.ui.register_page.show()

    # 注册
    def register_confirm_proc(self):
        if self.ui.register_username_input.text() == '':
            self.ui.register_info.setText("the UserName is None ! ")
            return 
        elif self.ui.register_email_input.text() == '':
            self.ui.register_info.setText("the Email is None ! ")
            return 
        elif self.ui.register_pwd_input.text() == '':
            self.ui.register_info.setText("the PassWord is None ! ")
            return
        elif self.ui.register_pwd_input_confirm.text() == '':
            self.ui.register_info.setText("the Confirm PassWord is None ! ")
            return
        elif self.ui.register_pwd_input_confirm.text() != self.ui.register_pwd_input.text():
            self.ui.register_info.setText("Entering the password twice is not the same ! ")
            return 
        else:
            self.ui.register_info.setText("")

        regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex,self.ui.register_email_input.text()):
            self.ui.register_info.setText("The email address entered is invalid ! ")
            return 
        else:
            self.ui.register_info.setText("")
        
        userinfo = self.userinfo_db.find_user_by_username(self.ui.register_username_input.text())
        if userinfo:
            self.ui.register_info.setText("The username you entered already exists ! ")
            return
        else:
            self.ui.register_info.setText("")

        md = hashlib.md5(self.ui.register_pwd_input_confirm.text().encode())
        md5pwd=md.hexdigest()
        self.userinfo_db.insert( 
            ["username","password","email","date"], 
            [ 
                self.ui.register_username_input.text(), 
                md5pwd, 
                self.ui.register_email_input.text(), 
                datetime.datetime.now().strftime('%y%m%d%H%M')
            ]
        )
        self.ui.register_info.setText("Congratulations, you have successfully registered ! ")
        
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

    # 登录
    def login_confirm_proc(self):
        global global_username,global_password,global_remember
        if self.ui.username_input.text() == '':
            self.ui.login_info.setText("the UserName is None ! ")
            return 
        elif self.ui.password_input.text() == '':
            self.ui.login_info.setText("the PassWord is None ! ")
            return
        else:
            self.ui.login_info.setText("")

        userinfo = self.userinfo_db.find_user_by_username(self.ui.username_input.text())
        if not userinfo :
            self.ui.login_info.setText("the user does not exist ! ")
            return
        else :
            md = hashlib.md5(self.ui.password_input.text().encode())
            md5pwd=md.hexdigest()
            if md5pwd == userinfo[0][1]:
                if self.ui.remember_box.isChecked():
                    global_username = self.ui.username_input.text()
                    global_password = self.ui.password_input.text()
                else:
                    global_username = ""
                    global_password = ""
                
                global_remember = self.ui.remember_box.isChecked()
                self.userinfo_db.update_by_username(self.ui.username_input.text(),["last"],[datetime.datetime.now().strftime('%y%m%d%H%M')])
                self.close()
                self.win = MainWindow(self.userinfo_db,self.lexilab_db)
            else:
                self.ui.login_info.setText("UserName is not match with PassWord ! ")


class MainWindow (QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False
    def __init__(self,userinfo_db,lexilab_db):
        super().__init__()

        self.userinfo_db = userinfo_db
        self.lexilab_db  = lexilab_db

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
        self.win = LoginWindow(self.userinfo_db,self.lexilab_db)

    def commit_btn_proc(self):
        print(self.ui.term_input.toPlainText())
        print(self.ui.explain_input.toPlainText())
        # self.sqlor.insert(["term","explain" ],[self.ui.term_input.toPlainText(),self.ui.explain_input.toPlainText()])
        
        print("commit")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    userinfo_db = SQLClass('./db/userinfo.db','userinfo')
    # userinfo_db.insert(["username","password","email","date"],["yyrwkk","81dc9bdb52d04dc20036dbd8313ed055","2962056732@qq.com","2403141253"])
    win = LoginWindow(userinfo_db,None)
    exit_code = app.exec_()
    
    userinfo_db.exit()
    sys.exit(exit_code)