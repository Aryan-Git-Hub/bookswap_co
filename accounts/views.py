from django.shortcuts import render, HttpResponseRedirect
# for authentication
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm, LoginForm, UserProfileForm, AddressForm
from accounts.models import CustomUser, Address
from django.contrib.auth.hashers import make_password, check_password
# for OTP
from django.core.mail import send_mail
import random
from django.conf import settings
# creating user cart
from books.models import Cart


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


def custom_authenticate(user_email, user_pass):
    try:
        user = CustomUser.objects.get(email=user_email)
        if(check_password(user_pass, user.password)):
            return user
        return None
    except:
        return None

# making custom decorator function
def not_auth_user(func):
    def ref(*args, **kwargs):
        req = args[0]
        if req.user.is_authenticated:    
            messages.warning(req, "You are already Logged in!!!")
            return HttpResponseRedirect('/')
        else:
            return func(*args, **kwargs)
    return ref


@not_auth_user
def signup(request):
    fm = SignupForm()
    if request.method=='POST':
        fm = SignupForm(request.POST)
        
        if fm.is_valid():
            email = fm.cleaned_data['email']
            password = fm.cleaned_data['password']
            confirm_password = fm.cleaned_data['confirm_password']
            if password==confirm_password:
                # # Generate OTP
                # otp = random.randint(100000, 999999)
                # # Send Email
                # subject = 'Your OTP for Account Verification'
                # message = f'Your OTP is {otp}'
                # sendEmail(email, subject, message)
                # return render(request, "accounts/verify.html", {'email': email, 'otp': otp})
                fm.fields['password'] = make_password(confirm_password)
                user = fm.save()
                # creating user cart
                Cart.objects.create(user=user)
                user.password = make_password(confirm_password)
                user.save()
                login(request, user)
                messages.success(request, 'Account Created Successfully!')
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Password and Confirm Password not matched!')
                return render(request, "accounts/signup.html", {'form': fm})
    return render(request, "accounts/signup.html", {'form': fm})


@not_auth_user
def auth_login(request):
    fm = LoginForm()
    if request.method=='POST':
        fm = LoginForm(request.POST)
        if fm.is_valid():
            email = fm.cleaned_data['email']
            password = fm.cleaned_data['password']
            user = custom_authenticate(email, password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged In Successfully!')
                return HttpResponseRedirect('/')
            
            messages.error(request, 'Invalid Credentials!')

    return render(request, "accounts/login.html", {'form': fm})


@login_required
def auth_logout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully!')
    return HttpResponseRedirect('/accounts/login/')


@login_required
def profile(request):
    fm = UserProfileForm(instance=request.user)
    user = CustomUser.objects.get(email=request.user.email)
    if request.method=="POST":
        fm = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if fm.is_valid():
            username = fm.cleaned_data["username"]
            mobile = fm.cleaned_data["mobile"]
            gender = fm.cleaned_data["gender"]
            photo = fm.cleaned_data["photo"]
            if((user.username==username) & (user.mobile==str(mobile)) & (user.gender==gender) & (user.photo==photo)):
                messages.warning(request, "Your profile is already updated!")
                return HttpResponseRedirect('/accounts/profile/')
            fm.save()
            messages.success(request, "Profile Updated!")
    return render(request, "accounts/profile.html", {"form":fm})



@login_required
def user_saved_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "accounts/user_saved_addresses.html", {"addresses":addresses})


@login_required
def add_address(request, book_id = 0):
    add_or_edit = "Add"
    inst = None
    if book_id:
        try:
            inst = Address.objects.get(id=book_id)
        except:
            messages.error(request, "Please try again!")
            return HttpResponseRedirect('/accounts/addresses/')
        add_or_edit = "Edit"
    fm = AddressForm(initial={"user":request.user}, instance=inst)

    if request.method=="POST":
        fm = AddressForm(request.POST, instance=inst)
        # setting city choices according to the state value
        try:
            state_val = request.POST.get("state", "")
            if state_val!="":
                import json
                with open("static/JSON/state_cities.json", "r") as f:
                    data = json.load(f)
                    for i in data:
                        if i["state"]==state_val:
                            fm.fields["city"].choices = i["cities"]
                            break;
        except:
            messages.error(request, "Please try again!")
        if fm.is_valid():
            fm.save()
            messages.success(request, "Address Saved Successfully!")
            return HttpResponseRedirect('/accounts/addresses/')
    return render(request, "accounts/add_address.html", {"form":fm, "add_or_edit":add_or_edit})