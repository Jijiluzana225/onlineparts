from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='orders/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', landing_page, name='home'),  # This makes the landing page accessible at "/"
    path('profile/update/', profile_update_view, name='profile_update'),
    path("order/", order_part_view, name="order_part"),
    path("order-success/", order_success, name="order_success"),
    path('part-requests/', part_request_list, name='part_request_list'),
    path('part-requests/<int:pk>/', part_request_detail, name='part_request_detail'),
    path("bid/<int:part_request_id>/", place_bid, name="place_bid"),
]

