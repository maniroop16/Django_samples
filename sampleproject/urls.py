"""
URL configuration for sampleproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from testingapp.views import test
from sendemail.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('sampleapp/',test, name = "test"),

    path('', base, name= 'base'),
    path('register/', register, name= 'register'),
    path('login/', login_page, name= 'login_page'),
    path('otp/',verify_otp, name = "verify_otp"),

    path('sendemail/', email_function, name = 'email_function'),
    
    path("website/", include('ecommerce.urls')),

    path('admin/', admin.site.urls),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)