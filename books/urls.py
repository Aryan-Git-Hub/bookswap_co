from django.urls import path
from books import views

urlpatterns = [
    path('', views.index, name='home'),
    path('checkout/', views.checkout, name='checkout'),
]