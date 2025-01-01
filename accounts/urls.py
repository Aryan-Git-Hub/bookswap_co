from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.auth_login, name='login'),
    path('logout/', views.auth_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('addresses/', views.user_saved_addresses, name='user_saved_addresses'),
    path('address/<int:book_id>/', views.add_address, name='add_address'),
]
