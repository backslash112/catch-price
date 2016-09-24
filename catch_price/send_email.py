#!/usr/bin/python
#coding:utf-8

import smtplib
from email.mime.text import MIMEText
import logging

class SendEmail:
    def send(self, title, link):

        text = '{0}: {1}'.format(title, link)
        msg = MIMEText(text, 'plain', 'utf-8')
        sender = '459455120@qq.com'
        receivers = 'yangcun@live.com'
        msg['Subject'] = '更新价格: {0}'.format(title)
        msg['From'] = sender
        msg['To'] = receivers

        server = smtplib.SMTP_SSL('smtp.qq.com')
        server.login('459455120@qq.com', '')
        server.sendmail(sender, [receivers], msg.as_string())
        server.quit()
