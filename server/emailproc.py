import yagmail

class EamilProc:

    def __init__(self,user,code,host="smtp.qq.com"):
        self.user = user
        self.code = code 
        self.host = host

        self.yag_server = yagmail.SMTP(user=self.user, password=self.code,host=self.host)

    
    def send_add_user_email(self,to,username):
        # 发送对象列表
        email_to = [to]
        email_title = '注册成功通知'
        email_content =  '''
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>注册成功通知</title>
            </head>
            <body style="font-family: Arial, sans-serif; background-color: #f1f1f1; text-align: center;">
                <div style="max-width: 600px; margin: auto auto; padding: 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <span style="font-size: 60px;">🐼</span>
                    <h1 style="color: #4CAF50;">恭喜，注册成功！</h1>
                    <p style="color: #4CAF50;">亲爱的%s，您已成功注册。</p>
                    <p style="color: #4CAF50;">欢迎加入LexiLab的大家庭，一起记录一起成长。</p>
                </div>
            </body>
        </html>'''%(username)
        # 附件列表
        #email_attachments = ['./attachments/report.png']
        # 发送邮件
        # self.yag_server.send(email_to, email_title, email_content, email_attachments)
        self.yag_server.send(to=email_to,subject=email_title,contents=email_content)

    def exit(self):
        self.yag_server.close()
        


