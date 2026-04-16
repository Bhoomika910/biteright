from django.urls import path
from .views import CreateUserProfileView, UserDetailView, UserListCreateView, AddressView

urlpatterns = [
    path('profile/', CreateUserProfileView.as_view(),   name='create-user-profile'),
    path('',         UserListCreateView.as_view(),      name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(),          name='user-detail'),
    path('<int:user_id>/addresses/', AddressView.as_view(), name='user-addresses'),
]
