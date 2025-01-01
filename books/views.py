from django.shortcuts import render, HttpResponseRedirect
from books.models import Book, ImageModel
from books.forms import BookForm, BookImageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# for search_results()
from django.db.models import Q

# Create your views here.
def index(request):
    all_books = Book.objects.all()
    return render(request, 'books/index.html', {"all_books":all_books})


@login_required
def checkout(request):
    return render(request, 'books/checkout.html')


@login_required
def post_ad(request):
    all_addresses = request.user.addresses.all()
    if len(all_addresses)==0:
        messages.error(request, "Please add an address first!")
        return HttpResponseRedirect('/accounts/address/0/')
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
    return render(request, "books/post_ad.html", {"form":fm, "book_image_form":book_image_fm, "addresses":all_addresses})


def user_posted_ads(request):
    user_ads = Book.objects.filter(seller=request.user)
    return render(request, "books/user_posted_ads.html", {"user_ads":user_ads})


def book_preview(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    if(book==None):
        return HttpResponseRedirect("/")
    user = request.user
    if((request.method=="POST") & (user.is_authenticated)):
        add_to_cart = request.POST.get("add_to_cart", None)
        if(add_to_cart=="true"):
            user.cart.cart_val += 1
            user.cart.books[str(book_id)] = 1
            # for increasing qty
            # if(user.cart.books.get(str(book_id))):
            #     user.cart.books[str(book_id)] += 1
            # else:
            #     user.cart.books[str(book_id)] = 1
            user.cart.save()
    return render(request, "books/book_preview.html", {"book":book})


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
    return render(request, "books/search_results.html", {"books":bks, "search_for":query})


@login_required
def cart(request):
    if request.method=="POST":
        import json
        from django.http import JsonResponse
        data_body = json.loads(request.body) # to convert string data into json object
        user_cart = request.user.cart

        # to add qty
        bk = Book.objects.get(id=data_body["book_id"])
        total_price = float(data_body["total_price"])
        qty = user_cart.books[str(data_body["book_id"])]
        if(data_body["inc_or_dec_or_rem"]=="increaseQuantity"):
            user_cart.books[str(data_body["book_id"])] += 1
            total_price += bk.price
            qty = user_cart.books[str(data_body["book_id"])]
            user_cart.cart_val += 1
            user_cart.save()
        
        # to decrease qty
        elif(data_body["inc_or_dec_or_rem"]=="decreaseQuantity"):
            user_cart.books[str(data_body["book_id"])] -= 1
            total_price -= bk.price
            qty = user_cart.books[str(data_body["book_id"])]
            if(qty<=0):
                del user_cart.books[str(data_body["book_id"])]
            if(qty>=0): user_cart.cart_val -= 1
            user_cart.save()
        
        # to delete book from cart
        
        elif(data_body["inc_or_dec_or_rem"]=="deleteBook"):
            total_price -= bk.price*qty
            user_cart.cart_val -= qty
            del user_cart.books[str(data_body["book_id"])]
            user_cart.save()
            
        return JsonResponse({"qty":qty, "total_price":total_price})
        
    bks = request.user.cart.books
    books = {}
    for book_id, qty in bks.items():
        books[Book.objects.get(id=int(book_id))] = qty
    return render(request, "books/cart.html", {"books":books})