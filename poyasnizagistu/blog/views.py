from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404

from .models import *


def home(request):
    return render(request, 'blog/home.html')


def blog(request):
    posts = Post.objects.all().order_by('-time_create')
    context = {
    'posts': posts,
    'cat_selected': 0
    }

    return render(request, 'blog/blog.html', context=context)


def show_post(request, post_slug):
    one_post = get_object_or_404(Post, slug=post_slug)

    return render(request, 'blog/post.html', {'one_post': one_post})

def show_category(request, cat_slug):
    posts = Post.objects.filter(cat__slug=cat_slug)

    context = {
    'posts': posts,
    'cat_selected': cat_slug
    }

    if len(posts) == 0:
        raise Http404()
    return render(request, 'blog/category.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
