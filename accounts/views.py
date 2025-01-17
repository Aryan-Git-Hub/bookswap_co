from django.shortcuts import render, HttpResponseRedirect, redirect
# for authentication
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm, LoginForm, UserProfileForm, AddressForm, OtpForm, ChangePassword
from accounts.models import CustomUser, Address
from django.contrib.auth.hashers import make_password, check_password
# for email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# for OTP
import random
from django.conf import settings
from django.utils.timezone import now, timedelta
from email.mime.image import MIMEImage
import os
# to convert time object to json serializable
from datetime import datetime
# creating user cart
from books.models import Cart


# Send Email Function
def sendEmail(to, subject, **kwargs):
    if to=='' or to==None:
        return False
    # Subject and sender
    subject = "Welcome to Our Service"
    from_email = settings.EMAIL_HOST_USER
    
    # Render the HTML content
    html_content = render_to_string('accounts/email_template.html', kwargs)
    text_content = strip_tags(html_content)  # Fallback plain text
    
    # Create the email
    email = EmailMultiAlternatives(subject, text_content, from_email, [to])
    email.attach_alternative(html_content, "text/html")

    # Attaching logo image
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.jpeg')
    with open(logo_path, 'rb') as logo_file:
        logo = MIMEImage(logo_file.read())
        logo.add_header('Content-ID', '<logo>')
        logo.add_header('Content-Disposition', 'inline', filename='logo.jpeg')
        email.attach(logo)
    
    # Send the email
    try:
        email.send()
        return True
    except:
        return False


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


def profile_completed_decorator(func):
    def modified_func(request, *args, **kwargs):
        previous_url_name = request.resolver_match.url_name
        if not request.user.profile_completed:
            messages.warning(request, "Please complete your profile first!")
            return HttpResponseRedirect('/accounts/profile/?next='+str(previous_url_name))
        
        return func(request, *args, **kwargs)
    return modified_func


def address_added_decorator(func):
    def modified_func(request, *args, **kwargs):
        previous_url_name = request.resolver_match.url_name
        if not request.user.address_added:
            messages.warning(request, "Please add an address first!")
            return HttpResponseRedirect('/accounts/address/0/?next='+str(previous_url_name))
        
        return func(request, *args, **kwargs)
    return modified_func


def generating_otp(request, email, otp_for, **kwargs):
    # Generate OTP
    otp = random.randint(100000, 999999)
    # Send Email
    subject = 'Your OTP for Account Verification'
    message = {"otp":otp, "username":kwargs.get("username")}
    if(sendEmail(email, subject, **message)==False):
        messages.error(request, "Please try again later!")
        return redirect("home")
    expiration_time = now() + timedelta(minutes=10)  # Set expiration to 10 minutes from now
    otp_session_dict = {"otp_for":otp_for, "otp":make_password(str(otp)), "email":email, "expiry":expiration_time.isoformat()}
    otp_session_dict.update(kwargs)
    request.session["otp_session_dict"] = otp_session_dict
    return redirect('otp')


@not_auth_user
def signup(request):
    fm = SignupForm()
    if request.method=='POST':
        fm = SignupForm(request.POST)
        
        if fm.is_valid():
            username = fm.cleaned_data['username']
            email = fm.cleaned_data['email']
            password = fm.cleaned_data['password']
            confirm_password = fm.cleaned_data['confirm_password']
            if password==confirm_password:
                additional_data = {"form":fm.cleaned_data, "username":username}
                return generating_otp(request, email, "signup", **additional_data)
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
                additional_data = {"username":user.username}
                return generating_otp(request, email, "login", **additional_data)
 
            messages.error(request, 'Invalid Credentials!')

    return render(request, "accounts/login.html", {'form': fm})


@login_required
def auth_logout(request):
    request.session.flush()
    logout(request)
    messages.success(request, 'Logged Out Successfully!')
    return HttpResponseRedirect('/accounts/login/')


@not_auth_user
def change_password(request):
    fm = ChangePassword()
    if request.method=="POST":
        fm = ChangePassword(request.POST)
        if fm.is_valid():
            email = fm.cleaned_data["email"]
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                messages.error(request, "User does not exist!")
                return redirect("change_pass")
            new_password = make_password(fm.cleaned_data["new_password"])
            additional_data = {"new_password":new_password, "username":user.username}
            return generating_otp(request, email, "change_pass", **additional_data)
    return render(request, "accounts/change_pass.html", {"form":fm})


@not_auth_user
def otp(request):
    otp_session_dict = request.session.get("otp_session_dict", None)
    if not otp_session_dict:
        return redirect('home')
    if now()>datetime.fromisoformat(otp_session_dict["expiry"]):
        messages.warning(request, "OTP is expired")
        return redirect('home')
    fm = OtpForm()
    if request.method=="POST":
        fm = OtpForm(request.POST)
        try:
            if fm.is_valid():
                form_otp = str(fm.cleaned_data.get("otp"))
                session_otp = otp_session_dict["otp"]
                varification = check_password(form_otp, session_otp)
                if varification:
                    # for which method we have to sent otp
                    if otp_session_dict["otp_for"]=="signup":
                        signup_fm = otp_session_dict["form"]
                        user = CustomUser.objects.create(
                            username = signup_fm.get("username"),
                            email = signup_fm.get("email"),
                            password = make_password(signup_fm.get("confirm_password")),
                        )
                        # creating user cart
                        Cart.objects.create(user=user)
                        login(request, user)
                        messages.success(request, 'Account Created Successfully!')
                        return HttpResponseRedirect('/')
                    
                    elif otp_session_dict["otp_for"]=="login":
                        email = otp_session_dict.get("email")
                        user = CustomUser.objects.get(email=email)
                        login(request, user)
                        messages.success(request, 'Logged In Successfully!')
                        return HttpResponseRedirect('/')
                    
                    elif otp_session_dict["otp_for"]=="change_pass":
                        email = otp_session_dict.get("email")
                        new_password = otp_session_dict.get("new_password")
                        user = CustomUser.objects.get(email=email)
                        user.set_password(new_password)
                        user.save()
                        messages.success(request, "Your password changed successfully!")
                        login(request, user)
                        return redirect('home')

                    del otp_session_dict
                messages.error(request, "OTP not varified!")
        except Exception as e:
            # print(e)
            messages.error(request, "Please try again later!")
            return redirect('home')
    return render(request, "accounts/otp.html", {"form":fm})


@login_required
def profile(request):
    fm = UserProfileForm(instance=request.user)
    user = CustomUser.objects.get(id=request.user.id)
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
            user = fm.save()
            user.profile_completed = True
            user.save()
            messages.success(request, "Profile Updated!")
            # Redirect to the previous pages
            next_url = request.GET.get('next', 'profile')
            return redirect(next_url)
    return render(request, "accounts/profile.html", {"form":fm})



@login_required
def user_saved_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    if len(addresses)==0:
        user = request.user
        user.address_added = False
        user.save()
    return render(request, "accounts/user_saved_addresses.html", {"addresses":addresses})


@login_required
def add_address(request, address_id = 0):
    add_or_edit = "Add"
    inst = None
    if address_id!=0:
        try:
            inst = Address.objects.get(id=address_id)
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
            request.user.address_added = True
            request.user.save()
            messages.success(request, "Address Saved Successfully!")
            # Redirect to the previous pages
            next_url = request.GET.get('next', 'user_saved_addresses')
            return redirect(next_url)
    return render(request, "accounts/add_address.html", {"form":fm, "add_or_edit":add_or_edit})



@login_required
def delete_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id)
        address.delete()
        messages.success(request, "Address Deleted Successfully!")
        user = request.user
        if len(Address.objects.filter(user=user))==0:
            user.address_added = False
            user.save()
    except:
        messages.error(request, "Please try again!")
    return HttpResponseRedirect('/accounts/addresses/')
