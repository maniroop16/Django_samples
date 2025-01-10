from django.contrib import admin
from .models import CustomAccount
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class ModifyUserFields(admin.StackedInline):
    model = CustomAccount
    can_delete = False
    verbose_name_plural = "Modify_User"

class CustomizeUser(UserAdmin):
    inlines = (ModifyUserFields,)

admin.site.unregister(User)
admin.site.register(User, CustomizeUser)

admin.site.register(CustomAccount)