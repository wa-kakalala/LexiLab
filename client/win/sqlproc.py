import sqlite3

class SQLClass:
    def __init__(self,dbpath,tablename):
        self.dbpath=dbpath
        self.tablename = tablename
        self.conn = None
        self.c = None
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.dbpath)
        self.c = self.conn.cursor()

    def insert(self,fileds=[],values=[]):
        key = ",".join(fileds)
        value =""
        for j in values:
            value = value+'"' +str(j) + '"'+","
        value = value[:-1]
        item = "INSERT INTO "+self.tablename+" ( "+  key+  " ) " + "VALUES (" + value +")"
        # print(item)
        self.c.execute(item)
        self.conn.commit()

    def check(self,name):
        self.c = self.conn.cursor()
        item = "SELECT term FROM "+ self.tablename
        print(item)
        explain_list= self.c.execute(item)
        print(explain_list)

    def find_user_by_username(self,username):
        self.c = self.conn.cursor()
        item = "SELECT * FROM " + self.tablename + " WHERE username = " + "'" + username + "'"
        # print(item)
        self.c.execute(item)
        userinfo = self.c.fetchall()
        print(userinfo)
        return userinfo
    def exit(self):
        self.c.close()
        self.conn.close()

    def update_by_username(self,username,fileds=[],values=[]):
        update_content = ' '
        for idx in range(len(fileds)-1):
            update_content += fileds[idx] + '=' +'"' + values[idx] + '",'
        update_content += fileds[-1] + '=' +'"' + values[-1] + '" '

        item = "UPDATE " + self.tablename + " set " + update_content + " WHERE username = " + "'" + username + "'"
        # print(item)
        self.c.execute(item)
        self.conn.commit()



