from django.urls import path

from .views import AppUserListView

app_name = 'users'
urlpatterns = [
    path('', AppUserListView.as_view(), name='list')
]
