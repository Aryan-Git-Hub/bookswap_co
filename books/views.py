from django.shortcuts import render
from books.models import Book

# Create your views here.
def index(request):
    all_books = Book.objects.all()
    return render(request, 'books/index.html', {"all_books":all_books})


def checkout(request):
    return render(request, 'books/checkout.html')