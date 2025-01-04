from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.auth_login, name='login'),
    path('logout/', views.auth_logout, name='logout'),
    path('change_pass/', views.change_password, name="change_pass"),
    path('otp/', views.otp, name='otp'),
    path('profile/', views.profile, name='profile'),
    path('addresses/', views.user_saved_addresses, name='user_saved_addresses'),
    path('address/<int:address_id>/', views.add_address, name='add_address'),
    path('addresses/remove/<int:address_id>/', views.delete_address, name='delete_address'),
]
