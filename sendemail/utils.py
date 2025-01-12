import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

def send_otp(request,username,email):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=120)
    otp = totp.now()

    request.session['otp_secret_key'] = totp.secret
    valid_time = datetime.now() + timedelta(minutes=2)
    request.session['otp_valid_date'] = str(valid_time)

    print(f'the otp is {otp}')

    subject = 'Website OTP Verification'
    description = f'''
    Dear {username},
    The OTP for verifying the login is {otp}.
    Note: Contact administrator if it is anonymous login
'''

    send_mail(
            subject, #subject of email
            description, # description of the email
            'settings.EMAIL_HOST_USER', # sender email
            [email], # Receiver email
            fail_silently= False
        )
