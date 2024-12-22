from django.shortcuts import render
# for OTP
from django.core.mail import send_mail
import random
from django.conf import settings


# Send Email Function
def sendEmail(to, subject, message):
    if to=='' or to==None:
        return False
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to],
        fail_silently=False
    )
    return True


# making custom decorator function
def signup(request):
    return render(request, "accounts/signup.html")

def login(request):
    return render(request, "accounts/login.html")