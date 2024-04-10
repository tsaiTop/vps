from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import re
import random
import smtplib
import string
import os

  # 发送邮件
  
def send_email_code(receiver_email: str, code: str):
    """
    @receiver_email: 接收者的邮箱
    @code: 验证码
    """
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    sender_name = os.getenv("SENDER_NAME")

    # 构建邮件内容
    message = MIMEMultipart()
    message["From"] = formataddr((sender_name, sender_email))
    message["To"] = receiver_email
    message["Subject"] = "验证码"  # 邮件主题
    
    # 邮件正文
    body = f"你的验证码是: {code}"

    message.attach(MIMEText(body, 'plain'))

    # 使用 SSL 连接 QQ 邮箱的 SMTP 服务器
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))
    finally:
        server.quit()

# 生成验证码
def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
  

# 判断输入字符串是否是合法的邮箱地址
def is_valid_email(email):
    """
    @email: 用户输入的邮箱地址
    """
    pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+$'
    if re.match(pattern, email):
        return True
    else:
        return False