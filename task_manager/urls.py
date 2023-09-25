from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from .views import HomeView, UserLoginView, UserLogoutView

# https://docs.djangoproject.com/en/4.1/topics/i18n/translation/#the-set-language-redirect-view
urlpatterns = [
    path('admin/', admin.site.urls),
] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', HomeView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('users/', include('task_manager.users.urls', namespace='users')),
    path('statuses/', include('task_manager.statuses.urls', namespace='statuses')),  # noqa: E501
    path('tasks/', include('task_manager.tasks.urls', namespace='tasks')),
    prefix_default_language=False,
)
