from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog
from PyQt5.QtCore import Qt,QPoint
from PyQt5 import QtCore
from PyQt5.QtGui  import QMouseEvent
import loginpage 
import mainpage
import dialogpage
from sqlproc import SQLClass,create_lexilab_db
import sys
import hashlib
import re
import datetime
from threading import Timer
import network
import resources_rc
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
import os

global_username = ''
global_password = ''
global_remember = False
global_lexilab_db = None
global_mainwindow = None

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
        # self.ui.register_page.hide()

        self.ui.stackedWidget.setCurrentIndex(1)
        # self.ui.login_page.show()

    def select_register_page_proc(self):
        self.ui.login_info.setText("")
        self.ui.register_info.setText("")
        # self.ui.login_page.hide()
        self.ui.stackedWidget.setCurrentIndex(0)

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

        create_lexilab_db(self.ui.register_username_input.text())
        
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
        global global_username,global_password,global_remember,global_lexilab_db
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
                if not os.path.exists('./db/%s_lexilab.db'%(self.ui.username_input.text())):
                     create_lexilab_db(self.ui.username_input.text())
            
                self.lexilab_db = SQLClass('./db/%s_lexilab.db'%(self.ui.username_input.text()),'lexilab')
                global_lexilab_db = self.lexilab_db
                self.close()
                self.win = MainWindow(self.userinfo_db,self.lexilab_db,self.ui.username_input.text())
                
            else:
                self.ui.login_info.setText("UserName is not match with PassWord ! ")

class DialogWindow(QDialog):
    def __init__(self,parent):
        super(DialogWindow,self).__init__(parent)
        self.ui = dialogpage.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.save_btn_proc)
        self.ui.pushButton_2.clicked.connect(self.discard_btn_proc)
        
        self.show()

    def save_btn_proc(self):
        self.done(1)

    def discard_btn_proc(self):
        self.done(2)
    
    



class MainWindow (QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False
    _tips = None
    _tipsIdx = 0
    _qgrapview_list = []

    def __init__(self,userinfo_db,lexilab_db,username):
        super().__init__()

        self.username = username

        self.userinfo_db = userinfo_db
        self.lexilab_db  = lexilab_db

        self.ui = mainpage.Ui_MainWindow()
        self.ui.setupUi(self)

        self._qgrapview_list = [self.ui.shownum_0,self.ui.shownum_1,self.ui.shownum_2,self.ui.shownum_3,self.ui.shownum_4,self.ui.shownum_5]

        self.ui.logout.clicked.connect(self.logout_btn_proc)
        self.ui.commit_btn.clicked.connect(self.commit_btn_proc)

        self.ui.home_btn.clicked.connect(self.show_home_page)
        self.ui.query_btn.clicked.connect(self.show_query_page)
        self.ui.person_btn.clicked.connect(self.show_person_page)

        self.ui.term_input.textChanged.connect(self.input_changed)
        # self.ui.setting_btn.clicked.connect(self.show_setting_page)

        self.ui.query_input.textChanged.connect(self.query_input_changed_proc)

        self.ui.search_btn.clicked.connect(self.search_btn_proc)
        self.show_home_page()

        self.show_tips("欢迎来到LexiLab系统, 请开始记录内容吧!")
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
            
    def input_changed(self):
        self.show_tips(" ")
            
    def logout_btn_proc(self):
        global global_lexilab_db
        self.lexilab_db.exit()
        global_lexilab_db = None
        self.close()
        self.win = LoginWindow(self.userinfo_db,self.lexilab_db)
    
    def timer_callback(self):
        if self._tipsIdx < len(self._tips):
            self.ui.tips.setText(self._tips[0:self._tipsIdx+1])
            self._tipsIdx += 1
            timer = Timer(0.1, self.timer_callback)
            timer.start()
        else:
            self._tips = ''
            self._tipsIdx = 0
            self.ui.commit_btn.setEnabled(True)

    def show_tips(self,tips):
        self._tips = tips
        self._tipsIdx = 0
        self.ui.commit_btn.setEnabled(False)
        timer = Timer(0.1, self.timer_callback)
        timer.start()

    def show_home_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def show_query_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_person_page(self):
        self.ui.show_username.setText(self.username)
        userinfo = self.userinfo_db.find_user_by_username(self.username)
        self.ui.show_email.setText(userinfo[0][2])


        count = self.lexilab_db.count_item_num()[0][0]
        count_str = "{:06}".format(count)
        # https://blog.csdn.net/springleaf2/article/details/122329284
        
        for idx in range(len(self._qgrapview_list)):
            sence = QGraphicsScene()
            item_idx = int(count_str[idx])
            frame = QImage(":/images/resources/images/number" + str(item_idx) + ".gif")
            item = QGraphicsPixmapItem(QPixmap.fromImage(frame))
            sence.addItem(item)
            self._qgrapview_list[idx].setScene(sence)

        self.ui.stackedWidget.setCurrentIndex(2)

    def show_setting_page(self):
        self.ui.stackedWidget.setCurrentIndex(3)

   
    def search_btn_proc(self):
        search_item = self.ui.query_input.toPlainText().strip()
        if( search_item == ""):
            return 
        
        item = self.lexilab_db.find_lexi_by_term(search_item)

        if item :
            self.ui.query_output.setPlainText(item[0][1])
        else :
            self.ui.query_output.setPlainText("暂时未添加该内容")
        pass
    def query_input_changed_proc(self):
        self.ui.query_output.setPlainText("")

    def commit_btn_proc(self):
        if self.ui.term_input.toPlainText().strip() == '':
            self.show_tips("输入术语栏不可以为空哦!")
            return 
        elif self.ui.explain_input.toPlainText() == '':
            self.show_tips("输入释义栏不可以为空哦!")
            return 
        lexicon = self.lexilab_db.find_lexi_by_term(self.ui.term_input.toPlainText().strip())
        if not lexicon:
            self.lexilab_db.insert(
                ["term","explain","date","time"], 
                [ 
                    self.ui.term_input.toPlainText().strip(), 
                    self.ui.explain_input.toPlainText(),
                    datetime.datetime.now().strftime('%y%m%d'), 
                    datetime.datetime.now().strftime('%H%M')
                ]
            )
            self.show_tips("恭喜你，添加记录成功！")
        else:
            dialog = DialogWindow(self)
            res = dialog.exec_()
            if res == 1:
                self.lexilab_db.update_by_term(
                    self.ui.term_input.toPlainText().strip(),
                    ["term","explain","date","time"], 
                    [ 
                    self.ui.term_input.toPlainText().strip(), 
                    self.ui.explain_input.toPlainText(),
                    datetime.datetime.now().strftime('%y%m%d'), 
                    datetime.datetime.now().strftime('%H%M')
                    ]
                )
                self.show_tips("恭喜你，更新记录成功！")

    def setProperty(self,userinfo_db,lexilab_db,username):
        self.userinfo_db = userinfo_db
        self.lexilab_db = lexilab_db
        self.username = username

if __name__ == "__main__":
    app = QApplication(sys.argv)
    userinfo_db = SQLClass('./db/userinfo.db','userinfo')
    # userinfo_db.insert(["username","password","email","date"],["yyrwkk","81dc9bdb52d04dc20036dbd8313ed055","2962056732@qq.com","2403141253"])
    win = LoginWindow(userinfo_db,None)
    netThread = network.NetworkClass()
    netThread.start()

    exit_code = app.exec_()
    userinfo_db.exit()
    if global_lexilab_db:
        global_lexilab_db.exit()

    netThread.exit()

    sys.exit(exit_code)