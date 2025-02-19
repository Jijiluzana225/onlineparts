from django.urls import path
from .views import register
from django.contrib.auth import views as auth_views
from views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='orders/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', landing_page, name='home'),  # This makes the landing page accessible at "/"
]
