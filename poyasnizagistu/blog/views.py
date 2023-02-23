from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from albums.models import Album
from articles.models import Article
from .forms import CommentForm
from .models import *
from .utils import PostMixin


def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-time_create')[:2].select_related('cat')
    articles = Article.objects.filter(is_published=True).order_by('-time_create')[:2].select_related('thematic')
    albums = Album.objects.filter(is_published=True).order_by('-time_create')[:2].select_related('organ_system')
    hi = HomeHi.objects.all()[0]
    context = {
        'title': 'Главная',
        'posts': posts,
        'articles': articles,
        'albums': albums,
        'hi': hi
        }

    return render(request, 'blog/home.html', context=context)
def about(request):
    context = {
        'title': 'О сайте',
        }

    return render(request, 'blog/about.html', context=context)

def thumbs(request):
    if request.POST.get('action') == 'thumbs':
        id = int(request.POST.get('postid'))
        button = request.POST.get('button')
        update = Post.objects.get(id=id)

        if update.thumbs.filter(id=request.user.id).exists():
            q = Votes_Post.objects.get(
                Q(post_id=id) & Q(user_id=request.user.id))
            evote = q.vote

            if evote == True:

                if button == 'thumbsup':

                    update.thumbsup = F('thumbsup') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

                if button == 'thumbsdown':

                    update.thumbsup = F('thumbsup') - 1
                    update.thumbsdown = F('thumbsdown') + 1
                    update.save()

                    q.vote = False
                    q.save(update_fields=['vote'])

                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

            pass

            if evote == False:

                if button == 'thumbsup':

                    update.thumbsup = F('thumbsup') + 1
                    update.thumbsdown = F('thumbsdown') - 1
                    update.save()

                    q.vote = True
                    q.save(update_fields=['vote'])

                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

                if button == 'thumbsdown':

                    update.thumbsdown = F('thumbsdown') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

        else:

            if button == 'thumbsup':
                update.thumbsup = F('thumbsup') + 1
                update.thumbs.add(request.user)
                update.save()

                new = Votes_Post(post_id=id, user_id=request.user.id, vote=True)
                new.save()
            else:

                update.thumbsdown = F('thumbsdown') + 1
                update.thumbs.add(request.user)
                update.save()

                new = Votes_Post(post_id=id, user_id=request.user.id, vote=False)
                new.save()

            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown

            return JsonResponse({'up': up, 'down': down})

    pass


class PostList(PostMixin, ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context


    def get_queryset(self):
        return Post.objects.annotate(number_of_comments=Count('comments_post', filter=Q(comments_post__status=True)))\
            .filter(is_published=True)\
            .order_by('-time_create').select_related('cat')


class PostDetail(SuccessMessageMixin, FormMixin, DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'
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
        obj = self.object
        context['title'] = 'Пост - ' + str(obj.title)

        def get_vote(self):
            votes = Votes_Post.objects.filter(user=self.request.user.id, post=obj)
            if len(votes) == 0:
                return 'not_vote'
            if len(votes) == 1:
                if votes[0].vote == 0:
                    return 'down'
                if votes[0].vote == 1:
                    return "up"
            else:
                raise TypeError('Ошибка в VotePost')
        context['vote_post'] = get_vote(self)

        comments = self.get_modereted_comments()
        context['comments'] = comments
        context['page_obj'] = comments


        return context

    def get_modereted_comments(self):
        queryset = self.object.comments_post.filter(status=True).select_related('author')
        paginator = Paginator(queryset, 6)
        page = self.request.GET.get('page')
        comments = paginator.get_page(page)
        return comments


class ShowCategory(PostMixin, ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    allow_empty = False
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Categories_Post.objects.get(slug=self.kwargs['cat_slug'])
        context['title'] = 'Категория - ' + str(c.name)

        context['cat_selected'] = c.slug
        return context
    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)\
            .annotate(number_of_comments=Count('comments_post', filter=Q(comments_post__status=True)))\
            .order_by('-time_create').select_related('cat')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class SearchPosts(PostMixin,ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        q = self.request.GET.get('q')
        words = "".join(q[0].upper()) + q[1:]
        return Post.objects.filter(title__icontains = words, is_published=True).annotate(number_of_comments=Count('comments_post', filter=Q(comments_post__status=True))).select_related('cat')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context['title'] = 'Поиск Постов'
        return context
