from django.urls import path

from .views import (ListTasksView, CreateTaskView, UpdateTaskView,
                    DeleteTaskView, ShowTaskView)

app_name = 'tasks'
urlpatterns = [
    path('', ListTasksView.as_view(), name='list'),
    path('<int:pk>/', ShowTaskView.as_view(), name='show'),
    path('create/', CreateTaskView.as_view(), name='create'),
    path('<int:pk>/update/', UpdateTaskView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteTaskView.as_view(), name='delete'),
]
