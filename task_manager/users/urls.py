from django.urls import path
from django.views import View

from .views import (
    ListUsersView,
    CreateUserView,
    UpdateUserView,
    DeleteUserView
)

app_name = 'users'
urlpatterns = [
    path('', ListUsersView.as_view(), name='list'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('<int:pk>/show/', View.as_view(), name='show'),
    path('<int:pk>/update/', UpdateUserView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteUserView.as_view(), name='delete'),
]
