from django.contrib import admin
from accounts.models import CustomUser, Address

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']


@admin.register(Address)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
