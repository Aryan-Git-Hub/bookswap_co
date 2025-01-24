from django import template

register = template.Library()


@register.filter
def total_price(books):
    try:
        total = 0
        for book, qty in books.items():
            total += float(book.price)*float(qty)
        return total
    except Exception as e:
        return 0
    

@register.filter
def book_in_cart(books_in_cart, book_id):
    try:
        if str(book_id) in books_in_cart:
            return True
    except:
        return 0


@register.filter
def book_in_wishlist(books_in_wishlist, book_id):
    try:
        if str(book_id) in books_in_wishlist:
            return True
        return False
    except:
        return 0