from django.urls import path

from .views import (
    ListLabelsView,
    CreateLabelView,
    UpdateLabelView,
    DeleteLabelView
)

app_name = 'labels'

urlpatterns = [
    path('', ListLabelsView.as_view(), name='list'),
    path('create/', CreateLabelView.as_view(), name='create'),
    path('<int:pk>/update/', UpdateLabelView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteLabelView.as_view(), name='delete'),
]
