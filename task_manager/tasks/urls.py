from django.urls import path

from .views import ListTaskView, CreateTaskView, UpdateTaskView, DeleteTaskView

app_name = 'tasks'
urlpatterns = [
    path('', ListTaskView.as_view, name='list'),
    path('create/', CreateTaskView.as_View, name='create'),
    path('<int:pk>/update/', UpdateTaskView.as_view, name='update'),
    path('<int:pk>/delete/', DeleteTaskView.as_view, name='delete'),
]