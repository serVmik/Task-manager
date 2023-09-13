from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from .views import HomeView

# https://docs.djangoproject.com/en/4.1/topics/i18n/translation/#the-set-language-redirect-view
urlpatterns = [
    path('admin/', admin.site.urls),
] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', HomeView.as_view(), name='home'),
    path('users/', include('task_manager.users.urls', namespace='users')),
)
