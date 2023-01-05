from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import *


def home(request):
    return render(request, 'blog/home.html')


def blog(request):
    post = Post.objects.all()
    return render(request, 'blog/blog.html', {'post': post})
