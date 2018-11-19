from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_active_email(token,username,email):
    subject = '我的书城用户激活'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<a href="http://192.168.13.34:8000/users/user_active/%s/">http://192.168.13.34:8000/users/user_active/</a>' % token
    send_mail(subject,message,sender,receiver,html_message=html_message)

