from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import *

menu = [{'title': "Блог", 'url_name': 'blog'},
{'title': "Статьи", 'url_name': 'home'},
{'title': "Альбомы", 'url_name': 'home'},
{'title': "Платное", 'url_name': 'home'},
{'title': "О сайте", 'url_name': 'home'},
]




def home(request):
    return render(request, 'blog/home.html', {'menu': menu})


def blog(request):
    post = Post.objects.all()
    return render(request, 'blog/blog.html', {'menu': menu, 'post': post})
