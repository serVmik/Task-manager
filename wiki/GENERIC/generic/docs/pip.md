## **[mkdocs](https://www.mkdocs.org/)**
[installing](https://www.mkdocs.org/user-guide/installation/#installing-mkdocs)
```cfgrlanguage
poetry add --group doc mkdocs
```
### [mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/#installation)
```cfgrlanguage
poetry add --group doc mkdocs-material
```
### [mkdocs-awesome-pages-plugin](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin#mkdocs-awesome-pages-plugin-)
[installing](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin#installation)
```cfgrlanguage
poetry add --group doc mkdocs-awesome-pages-plugin
```


## [Sphinx](https://docs.readthedocs.io/en/stable/index.html)
[install](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html#quick-start)
```cfgrlanguage
poetry add --group doc sphinx
```
[Install Using Markdown with Sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html#using-markdown-with-sphinx)
```
poetry add --group doc myst-parser
```
[Example projects](https://docs.readthedocs.io/en/stable/examples.html#example-projects)


## [jupyter-notebook](https://jupyter.org/install#jupyter-notebook)
```cfgrlanguage
poetry add --group shell notebook==6.5.6
```

To integrate ```notebook``` with ```Django``` you need to install [django-extensions](#django-extensions)   
To run the notebook:
```cfgrlanguage
jupyter notebook
```
> Run shell:  
> Новый / Django Shell-Plus



## [django-extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#installing)
```cfgrlanguage
poetry add --group shell django-extensions
```
[Configuration](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration)
```cfgrlanguage
INSTALLED_APPS = (
    ...
    'django_extensions',
    ...
)
```
```cfgrlanguage
poetry run ./manage.py collectstatic
```