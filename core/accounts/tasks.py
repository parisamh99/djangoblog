from celery import shared_task
from time import sleep

@shared_task
def SendEmail():
    sleep(2)
    print('done sending email')
