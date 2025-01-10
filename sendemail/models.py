from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobileNumber = models.CharField(max_length=10)
    DOB = models.DateField()
    gender = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username
    
