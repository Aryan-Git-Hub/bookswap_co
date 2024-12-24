from django.contrib import admin
from books.models import Book

# Register your models here.
@admin.register(Book)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'book_name']