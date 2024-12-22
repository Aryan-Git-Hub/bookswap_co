from django.shortcuts import render
# for authentication
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm
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


def signup(request):
    if request.method=='POST':
        fm = SignupForm(request.POST)
        print(fm)
        if fm.is_valid():
            email = fm.cleaned_data['email']
            password = fm.cleaned_data['password']
            confirm_password = fm.cleaned_data['confirm_password']
            if password==confirm_password:
                # Generate OTP
                otp = random.randint(100000, 999999)
                # Send Email
                subject = 'Your OTP for Account Verification'
                message = f'Your OTP is {otp}'
                sendEmail(email, subject, message)
                return render(request, "accounts/verify.html", {'email': email, 'otp': otp})
            else:
                return render(request, "accounts/signup.html", {'form': fm, 'error': 'Password and Confirm Password not matched!'})
    else:
        fm = SignupForm()
    return render(request, "accounts/signup.html", {'form': fm})

def login(request):
    return render(request, "accounts/login.html")