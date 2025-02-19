from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(PartRequest)
admin.site.register(Customer)

admin.site.register(User, UserAdmin)  # Register with UserAdmin for better UI