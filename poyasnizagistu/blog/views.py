from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import CommentForm
from .models import *


def home(request):
    return render(request, 'blog/home.html')



class BlogPosts(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context


    def get_queryset(self):
        return Post.objects.annotate(number_of_comments=Count('comments_post', filter=Q(comments_post__status=True)))

# def blog(request):
#     posts = Post.objects.all().order_by('-time_create')
#
#     context = {
#     'posts': posts,
#     'cat_selected': 0
#     }
#
#
#     return render(request, 'blog/blog.html', context=context)




class ShowBlogPost(SuccessMessageMixin, FormMixin, DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'one_post'
    slug_url_kwarg = 'post_slug'

    form_class = CommentForm
    success_message = 'Комментарий успешно отправлен! Ожидайте проверку модератором!'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'post_slug': self.get_object().slug})


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пост - ' + str(context['one_post'])
        context['comments'] = CommentsPost.objects.filter(post_id__slug=context['one_post'].slug, status=True)

        return context

# def show_post(request, post_slug):
#     one_post = get_object_or_404(Post, slug=post_slug)
#     comments = CommentsPost.objects.filter(post__slug=post_slug)
#     form = CommentForm(request.POST)
#
#     return render(request, 'blog/post.html', {'one_post': one_post, 'comments':comments, 'form':form})


class ShowBlogCategory(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    allow_empty = False
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat.slug
        return context
    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).annotate(number_of_comments=Count('comments_post', filter=Q(comments_post__status=True)))


# def show_category(request, cat_slug):
#     posts = Post.objects.filter(cat__slug=cat_slug)
#
#     context = {
#     'posts': posts,
#     'cat_selected': cat_slug
#     }
#
#     if len(posts) == 0:
#         raise Http404()
#     return render(request, 'blog/category.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
