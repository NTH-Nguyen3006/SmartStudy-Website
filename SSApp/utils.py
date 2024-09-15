from django.core.mail import send_mail
from django.conf import settings

def send_mail_to_user(email):
    emails = ["nthn300607@gmail.com"]
    if email: 
        emails.append(email)
    subject = 'This mail is test from django SSBot'
    message = 'This mail is test from django SSBot message'
    from_mail = settings.EMAIL_HOST_USER
    recipient_list = emails
    
    send_mail(subject, message, from_mail, recipient_list)