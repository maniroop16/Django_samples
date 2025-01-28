from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages 
from .models import CustomAccount
from django.contrib.auth import authenticate, login, logout
from testingapp.templates import *
from .utils import send_otp
from datetime import datetime
import pyotp
from ecommerce.urls import *
# Create your views here.


def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        mobilenumber = request.POST['mobilenumber']
        DOB = request.POST['DOB']
        gender = request.POST['gender']

        #print(firstname,lastname,username,email,mobilenumber,DOB,gender)

        user = User.objects.filter(username = username)
        if user.exists():
            messages.warning(request, "User already exists")
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = firstname,
            last_name = lastname,
            username = username,
            email = email
        )
        user.set_password(password)
        user.save()

        CustomAccount.objects.create(
            user = user,
            mobileNumber = mobilenumber,
            DOB = DOB,
            gender = gender
        )
        messages.success(request, 'Account Created Successfully')
        subject = "Account Registration Alert"
        description = f""" 
        Dear {username},
        This is to inform you that, You have created an Account on our website
        """
        send_mail(
            subject, #subject of email
            description, # description of the email
            'settings.EMAIL_HOST_USER', # sender email
            [email], # Receiver email
            fail_silently= False
        )
        messages.success(request, 'Email Sent successfully')
        return redirect('/register/')    
    return render(request, 'register.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username = username).exists():
            messages.warning(request, 'User Does not Exists/ Invalid User')
            return redirect('/login/')

        user = authenticate(username=username,password=password)

        if user is None:
            messages.warning(request, 'Invalid Password')
            return redirect('/login/')
        else:
            email = User.objects.filter(username = username)[0].email
            send_otp(request,username,email)
            request.session['username'] = username
            #login(request, user)
            return redirect('/otp/')

    return render(request , 'login.html')


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST['OTP']
        username = request.session['username']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            otp_valid_until = datetime.fromisoformat(otp_valid_date)
            
            if otp_valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=120)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    
                    return redirect('/website/')
                else:
                    messages.warning(request, "Incorrect OTP")
            else:
                messages.warning(request, "OTP time limit exceeded/ Expired")
        else:
            messages.warning(request, "Something went wrong!!")        

    return render(request , 'otp.html')



def email_function(request):
    if request.method == "POST":
        subject = request.POST['subject']
        email = request.POST['email']
        description = request.POST['description']

        print(subject, email, description)

        send_mail(
            subject, #subject of email
            description, # description of the email
            'settings.EMAIL_HOST_USER', # sender email
            [email], # Receiver email
            fail_silently= False
        )

        return redirect('/sendemail/')

    return render(request , 'email.html')