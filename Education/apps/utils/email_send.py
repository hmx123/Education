from  random import Random
from django.core.mail import send_mail
from django_redis import get_redis_connection

from Education.settings import EMAIL_FROM

from users.models import EmailVerifyRecord


def random_str(random_length=8):
    str = ''
    # 生成字符串可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

def send_register_email(email, send_type='register'):
    # 使用redis记录验证码 设置过期时间
    # con = get_redis_connection("default")
    # code = random_str(16)
    # con.setex(code, email, expriation_time)
    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    # 定制邮件内容
    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '用户注册激活邮件'
        email_body = '请点击下面链接激活你的账号： http://127.0.0.1:8000/active/{0}'.format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass
    if send_type == 'forget':
        email_title = '用户找回密码邮件'
        email_body = '请点击下面链接找回你的密码： http://127.0.0.1:8000/active/{0}'.format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass
