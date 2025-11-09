from django.shortcuts import render
from django.http import HttpResponse
import time
from .tasks import SendEmail

def send_email(request):
    SendEmail.delay()
    return HttpResponse("<h2>sending email</h2>")
    
