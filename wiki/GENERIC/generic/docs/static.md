# [Static Files](https://docs.djangoproject.com/en/5.0/ref/settings/#static-files)

Create a dir `media/` in the directory where the project is located (BASE_DIR).
```cfgrlanguage


```

`urls.py`
```cfgrlanguage
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

`settings.py`
```cfgrlanguage
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    # "/home/special.polls.com/polls/static",
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
```

Run
```cfgrlanguage
poetry run ./manage.py makemigrations
poetry run ./manage.py migrate
poetry run ./manage.py collectstatic
```

