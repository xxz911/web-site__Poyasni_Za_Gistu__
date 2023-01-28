from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin


from .forms import CommentForm
from .models import *
from .utils import DataMixin


def home(request):
    return render(request, 'blog/home.html')

def PostLikeView(request, post_slug):
    one_post = get_object_or_404(Post, slug=post_slug)
    if one_post.likes.filter(id=request.user.id).exists():
        one_post.likes.remove(request.user)
    else:
        one_post.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BlogPosts(DataMixin, ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context


    def get_queryset(self):
        return Post.objects.annotate(number_of_comments=Count('comments_post', filter=Q(comments_post__status=True)))\
            .annotate(likeds=Count('likes', filter=Q(likes=self.request.user.id)))\
            .filter(is_published=True)\
            .order_by('-time_create')

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
    def get_context_data(self, **kwargs):
        context = super(ShowBlogPost, self).get_context_data(**kwargs)
        context['title'] = 'Пост - ' + str(context['one_post'])
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        context['total_likes'] = post.get_total_likes()

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['liked'] = liked
        comments = self.get_modereted_comments()
        context['comments'] = comments
        context['page_obj'] = comments
        return context

    def get_modereted_comments(self):
        queryset = self.object.comments_post.filter(status=True)
        paginator = Paginator(queryset, 6)  # paginate_by
        page = self.request.GET.get('page')
        comments = paginator.get_page(page)
        return comments



# def show_post(request, post_slug):
#     one_post = get_object_or_404(Post, slug=post_slug)
#     comments = CommentsPost.objects.filter(post__slug=post_slug)
#     form = CommentForm(request.POST)
#
#     return render(request, 'blog/post.html', {'one_post': one_post, 'comments':comments, 'form':form})


class ShowBlogCategory(DataMixin, ListView):
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
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)\
            .annotate(number_of_comments=Count('comments_post', filter=Q(comments_post__status=True)))\
            .annotate(likeds=Count('likes', filter=Q(likes=self.request.user.id)))\
            .order_by('-time_create')


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
