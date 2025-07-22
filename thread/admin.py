from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(ThreadSubscription)
