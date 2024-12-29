from django.urls import path
from books import views

urlpatterns = [
    path('', views.index, name='home'),
    path('post/', views.post_ad, name='post_ad'),
    path('user-ads/', views.user_posted_ads, name='user_posted_ads'),
    path('book-view/<int:book_id>/', views.book_preview, name='book_preview'),
    path('search/', views.search_results, name="search_results"),
    path('cart/', views.cart, name='cart'),
]