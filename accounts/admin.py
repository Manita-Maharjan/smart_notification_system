from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User)
admin.site.register(LoginHistory)

# Register your models here.
