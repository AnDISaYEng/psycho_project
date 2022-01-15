from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_task(users):
    print(users)
    send_mail('Вы гей', 'Да-да, вы гей', 'test@gmail.com', users[1:])
