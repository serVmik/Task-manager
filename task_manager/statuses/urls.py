from django.urls import path

from task_manager.statuses.views import (
    ListStatusesView,
    CreateStatusView,
    UpdateStatusView,
    DeleteStatusView
)

app_name = 'statuses'
urlpatterns = [
    path('', ListStatusesView.as_view(), name='list'),
    path('create/', CreateStatusView.as_view(), name='create'),
    path('<int:pk>/update/', UpdateStatusView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteStatusView.as_view(), name='delete'),
]
