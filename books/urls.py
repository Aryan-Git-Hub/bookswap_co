from django.urls import path
from books import views

urlpatterns = [
    path('', views.index, name='home'),
    path('post/', views.post_ad, name='post_ad'),
    path('user-ads/', views.user_posted_ads, name='user_posted_ads'),
    path('book-view/<int:book_id>/', views.book_preview, name='book_preview'),
    path('search/', views.search_results, name="search_results"),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('orders/', views.your_orders, name='orders'),
    path('orders/<int:order_id>/', views.track_your_order, name='track_order'),
]