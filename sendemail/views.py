from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def email_function(request):
    if request.method == "POST":
        subject = request.POST['subject']
        email = request.POST['email']
        description = request.POST['description']

        send_mail(
            subject, #subject of email
            description, # description of the email
            'settings.EMAIL_HOST_USER', # sender email
            [email], # Receiver email
            fail_silently= False
        )

        return redirect('/sendemail/')

    return render(request , 'email.html')
