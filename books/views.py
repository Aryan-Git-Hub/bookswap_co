from django.shortcuts import render, HttpResponseRedirect, redirect
from books.models import Book, ImageModel
from books.forms import BookForm, BookImageForm, BookAdEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# for search_results()
from django.db.models import Q
# for user_posted_ads()
from django.http import JsonResponse
from accounts.views import profile_completed_decorator, address_added_decorator

# Create your views here.
def index(request):
    all_books = Book.objects.all()
    return render(request, 'books/index.html', {"all_books":all_books})


@login_required
def checkout(request):
    return render(request, 'books/checkout.html')


@login_required
@profile_completed_decorator
@address_added_decorator
def post_ad(request):
    all_addresses = request.user.addresses.all()
    fm = BookForm(initial={'seller': request.user})
    ADDRESS_CHOICES = []
    for address in all_addresses:
        ADDRESS_CHOICES.append([address.id, address.id])
    book_image_fm = BookImageForm()
    if request.method=="POST":
        fm = BookForm(request.POST)
        fm.fields["selected_address_id"].choices = ADDRESS_CHOICES
        book_image_fm = BookImageForm(request.POST, request.FILES)
        image_files = request.FILES.getlist("images")
        # limiting image selection
        if(len(image_files)>4):
            book_image_fm.add_error("images", "You can upload a maximum of 4 images.")
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
    return render(request, "books/post_ad.html", {"form":fm, "book_image_form":book_image_fm, "addresses":all_addresses})


@login_required
def user_posted_ads(request):
    fm = BookAdEditForm()
    user_ads = Book.objects.filter(seller=request.user)
    if request.method=="POST":
        # to sending instance to template
        if request.POST.get("action", None)=='edit':
            bk = Book.objects.get(id=request.POST.get("book_id"))
            request.session["book_id"] = bk.id
            fm = BookAdEditForm(instance=bk)
            return JsonResponse({"form":fm.as_div()})


        fm = BookAdEditForm(request.POST)
        if fm.is_valid():
            bk = Book.objects.get(id=request.session["book_id"])
            del request.session["book_id"]
            data_changes = fm.cleaned_data
            if bk.book_name==data_changes["book_name"] and bk.author==data_changes["author"] and bk.desc==data_changes["desc"] and bk.edition==data_changes["edition"] and bk.publication==data_changes["publication"] and bk.category==data_changes["category"] and bk.pages==data_changes["pages"] and bk.price==data_changes["price"]:
                messages.warning(request, "No changes made!")
                return JsonResponse({"success":True})
            bk.book_name = data_changes["book_name"]
            bk.author = data_changes["author"]
            bk.desc = data_changes["desc"]
            bk.edition = data_changes["edition"]
            bk.publication = data_changes["publication"]
            bk.category = data_changes["category"]
            bk.pages = data_changes["pages"]
            bk.price = data_changes["price"]
            bk.save()
            messages.success(request, "Ad Updated Successfully!")
            return JsonResponse({"success":True})
        return JsonResponse({"success":False, "form":fm.as_div()})
        
    return render(request, "books/user_posted_ads.html", {"user_ads":user_ads, "form":fm})


def book_preview(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    return render(request, "books/book_preview.html", {"book":book})


@login_required
def add_to_cart(request, book_id):
    user = request.user
    previous_url = request.META.get('HTTP_REFERER', '/')
    if not user.cart.books.get(str(book_id), None):
        print("hello")
        user.cart.cart_val += 1
        user.cart.books[str(book_id)] = 1
        # for increasing qty
        # if(user.cart.books.get(str(book_id))):
        #     user.cart.books[str(book_id)] += 1
        # else:
        #     user.cart.books[str(book_id)] = 1
        user.cart.save()
        messages.success(request, "Book added to cart!")
    else:
        messages.warning(request, "Book already added in cart!")
    return HttpResponseRedirect(previous_url)

def search_results(request):
    query = request.GET.get("search_for")
    bks = Book.objects.all()

    if query:
        bks = bks.filter(
            Q(book_name__icontains=query) | Q(desc__icontains=query) | Q(category__icontains=query) | Q(author__icontains=query) | Q(publication__icontains=query)
        )
    else:
        query = ""
        bks = None
    return render(request, "books/search_results.html", {"all_books":bks, "search_for":query})


@login_required
def cart(request):
    if request.method=="POST":
        import json
        from django.http import JsonResponse
        data_body = json.loads(request.body) # to convert string data into json object
        user_cart = request.user.cart

        
        bk = Book.objects.get(id=data_body["book_id"])
        total_price = float(data_body["total_price"])
        qty = user_cart.books[str(data_body["book_id"])]
        # to delete book from cart        
        if(data_body["inc_or_dec_or_rem"]=="deleteBook"):
            total_price -= bk.price*qty
            user_cart.cart_val -= qty
            del user_cart.books[str(data_body["book_id"])]
            user_cart.save()
        # to add qty
        # elif(data_body["inc_or_dec_or_rem"]=="increaseQuantity"):
        #     user_cart.books[str(data_body["book_id"])] += 1
        #     total_price += bk.price
        #     qty = user_cart.books[str(data_body["book_id"])]
        #     user_cart.cart_val += 1
        #     user_cart.save()
        # to decrease qty
        # elif(data_body["inc_or_dec_or_rem"]=="decreaseQuantity"):
        #     user_cart.books[str(data_body["book_id"])] -= 1
        #     total_price -= bk.price
        #     qty = user_cart.books[str(data_body["book_id"])]
        #     if(qty<=0):
        #         del user_cart.books[str(data_body["book_id"])]
        #     if(qty>=0): user_cart.cart_val -= 1
        #     user_cart.save()
        return JsonResponse({"qty":qty, "total_price":total_price})
        
    bks = request.user.cart.books
    books = {}
    for book_id, qty in bks.items():
        books[Book.objects.get(id=int(book_id))] = qty
    return render(request, "books/cart.html", {"books":books})
    


def your_orders(request):
    return render(request, "books/orders.html")
