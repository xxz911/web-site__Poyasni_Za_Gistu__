"""poyasnizagistu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from blog.views import home, pageNotFound, about



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about', about, name='about'),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('albums/', include('albums.urls')),
    path('articles/', include('articles.urls')),

# Путь для редактора ckeditor в админке
    re_path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Путь Django Debug Toolbar (работает только в режиме отладки)
if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Переопределяем метод обработки ошибки 404
handler404 = pageNotFound