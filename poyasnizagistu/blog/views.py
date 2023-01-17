from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render


from .models import *


def home(request):
    return render(request, 'blog/home.html')


def blog(request):
    posts = Post.objects.all().order_by('-time_create')
    cats = CategoryPost.objects.all()
    context = {
    'cats':cats,
    'posts': posts,
    'cat_selected': 0
    }

    return render(request, 'blog/blog.html', context=context)


def show_post(request, post_id):
    one_post = Post.objects.get(pk=post_id)

    return render(request, 'blog/post.html', {'one_post': one_post})

def show_category(request, cat_id):
    posts = Post.objects.filter(cat=cat_id).order_by('-time_create')
    cats = CategoryPost.objects.all()
    context = {
    'cats':cats,
    'posts': posts,
    'cat_selected': cat_id
    }

    if len(posts) == 0:
        raise Http404()
    return render(request, 'blog/category.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
