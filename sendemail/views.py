from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages 
from .models import CustomAccount
from django.contrib.auth import authenticate, login, logout
from testingapp.templates import *
# Create your views here.

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

        print(firstname,lastname,username,email,mobilenumber,DOB,gender)

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
        print(email)
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
            login(request, user)
            return redirect('/sampleapp/')

    return render(request , 'login.html')

