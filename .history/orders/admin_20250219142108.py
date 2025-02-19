from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(PartRequest)
admin.site.register(Customer)

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("part_request", "store", "price", "status", "created_at")
    list_filter = ("status", "created_at")