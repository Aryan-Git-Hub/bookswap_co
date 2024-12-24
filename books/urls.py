from django.urls import path
from books import views

urlpatterns = [
    path('', views.index, name='home'),
    path('post/', views.post_ad, name='post_ad'),
    path('checkout/', views.checkout, name='checkout'),
]