from django.contrib import admin
from books.models import Book, ImageModel, Cart

# Register your models here.
@admin.register(Book)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'book_name']


@admin.register(ImageModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'book']


@admin.register(Cart)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart_val']