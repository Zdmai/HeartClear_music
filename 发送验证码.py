import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# 创建邮件主体对象
email = MIMEMultipart()
# 设置发件人、收件人和主题
email['From'] = '18107155387@163.com'
email['To'] = '2580324258@qq.com'
email['Subject'] = Header('主题', 'utf-8')
# 添加邮件正文内容
content = """test for the send the code to the email!"""
email.attach(MIMEText(content, 'plain', 'utf-8'))
# 创建SMTP_SSL对象（连接邮件服务器）
smtp_obj = smtplib.SMTP_SSL('smtp.163.com', 465)
# 通过用户名和授权码进行登录
smtp_obj.login('18107155387@163.com', 'YONWGQPISLRJDIFI')
# 发送邮件（发件人、收件人、邮件内容（字符串））
smtp_obj.sendmail(
    '18107155387@163.com',
    '2580324258@qq.com',
    email.as_string()
)
