from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def total_price(books):
    try:
        total = 0
        for book, qty in books.items():
            total += float(book.price)*float(qty)
        return total
    except Exception as e:
        print(e)
        return 0