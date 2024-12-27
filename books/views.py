from django.shortcuts import render, HttpResponseRedirect
from books.models import Book, ImageModel
from books.forms import BookForm, BookImageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    all_books = Book.objects.all()
    return render(request, 'books/index.html', {"all_books":all_books})


@login_required
def checkout(request):
    return render(request, 'books/checkout.html')


@login_required
def post_ad(request):
    fm = BookForm(initial={'seller': request.user})
    book_image_fm = BookImageForm()
    if request.method=="POST":
        fm = BookForm(request.POST)
        book_image_fm = BookImageForm(request.POST, request.FILES)
        image_files = request.FILES.getlist("images")
        # setting city choices according to the state value
        try:
            state_val = request.POST.get("state", "")
            if state_val!="":
                import json
                with open("static/JSON/state_cities.json", "r") as f:
                    data = json.load(f)
                    for i in data:
                        if i["state"]==state_val:
                            fm.fields["city"].choices = i["cities"]
                            break;
        except Exception as e:
            messages.error(request, "Please try again!")
            return HttpResponseRedirect('/post/')
        if int(request.POST.get('seller'))!=request.user.id:
            messages.error(request, "Please try again!")
            return HttpResponseRedirect('/post/')
        elif fm.is_valid() & book_image_fm.is_valid():
            book = fm.save()
            for image in image_files:
                ImageModel.objects.create(book=book, image=image)
            messages.success(request, "Your Ad is now Published!")
            return HttpResponseRedirect('/')
    return render(request, "books/post_ad.html", {"form":fm, "book_image_form":book_image_fm})


def user_posted_ads(request):
    user_ads = Book.objects.filter(seller=request.user)
    return render(request, "books/user_posted_ads.html", {"user_ads":user_ads})


def book_view(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    if(book==None):
        return HttpResponseRedirect("/")
    return render(request, "books/book_preview.html", {"book":book})