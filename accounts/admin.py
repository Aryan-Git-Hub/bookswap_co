from django.contrib import admin
from accounts.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
