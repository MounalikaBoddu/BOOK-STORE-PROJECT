from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Order
from django.db.models import Sum

# Show all books on homepage
def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})

# Show detail of a single book
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_details.html', {'book': book})  # NOTE: use .html

# Add book to cart
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        Order.objects.create(book=book, quantity=quantity)
        return redirect('cart')
    return redirect('book_detail', book_id=book_id)

def cart(request):
    orders = Order.objects.all()
    total = sum(order.total_price() for order in orders)
    return render(request, 'cart.html', {'orders': orders, 'total_price': total})

def analytics(request):
    total_sales = Order.objects.count()
    total_revenue = sum(order.total_price() for order in Order.objects.all())
    top_books = Order.objects.values('book__title').annotate(total_qty=Sum('quantity')).order_by('-total_qty')[:5]
    return render(request, 'analytics.html', {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'top_books' : top_books
    })


