from django.shortcuts import render, HttpResponseRedirect
from books.models import Book
from books.forms import BookForm
from django.contrib import messages

# Create your views here.
def index(request):
    all_books = Book.objects.all()
    return render(request, 'books/index.html', {"all_books":all_books})


def checkout(request):
    return render(request, 'books/checkout.html')


def post_ad(request):
    fm = BookForm()
    if request.method=="POST":
        fm = BookForm(request.POST, request.FILES)
        print(fm)
        print(request.FILES)
        if fm.is_valid():
            messages.success(request, "Your Ad is now Published!")
            return HttpResponseRedirect('/')
    return render(request, "books/post_ad.html", {"form":fm})