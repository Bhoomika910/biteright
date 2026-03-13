from django.urls import path
from .views import CreateUserProfileView, UserDetailView, UserListCreateView

urlpatterns = [
    path('profile/', CreateUserProfileView.as_view(), name='create-user-profile'),
    path('',         UserListCreateView.as_view(),    name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(),        name='user-detail'),
]
