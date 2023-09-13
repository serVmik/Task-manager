from django.urls import path, include

from .views import AppUserListView

app_name = 'users'
urlpatterns = [
    path('', AppUserListView.as_view(), name='list')
]
