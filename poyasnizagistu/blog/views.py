from django.http import HttpResponse
from django.shortcuts import render
from .models import *


menu = ['Блог', 'Статьи', 'Альбомы', 'Платное', 'О сайте']


def home(request):
    return render(request, 'blog/home.html', {'menu': menu})


def blog(request):
    post = Post.objects.all()
    return render(request, 'blog/blog.html', {'menu': menu, 'post': post})
