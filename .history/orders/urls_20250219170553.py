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
    path("my-part-requests/", MyPartRequestsView.as_view(), name="my_part_requests"),
    path("bid_details/<int:pk>/", BidDetailView.as_view(), name="bid_detail"),
    path("accept-bid/<int:pk>/", AcceptBidView.as_view(), name="accept_bid"),
    path("store/bids/", store_bids, name="store_bids"),
    
    path("bidview/<int:pk>/", BidDetailView.as_view(), name="bid_detail_view"),
    path("bidview/<int:pk>/update/", BidUpdateView.as_view(), name="bid_update"),
    path("bidview/<int:pk>/delete/", BidDeleteView.as_view(), name="bid_delete"),
    
    
]

