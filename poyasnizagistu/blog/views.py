from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q, F
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin


from .forms import CommentForm
from .models import *
from .utils import PostMixin


def home(request):
    return render(request, 'blog/home.html')

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
        context['title'] = 'Пост - ' + str(context['post'])
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        def get_vote(self):
            votes = Votes_Post.objects.filter(user=self.request.user.id, post=post)
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
        queryset = self.object.comments_post.filter(status=True)
        paginator = Paginator(queryset, 6)
        page = self.request.GET.get('page')
        comments = paginator.get_page(page)
        return comments



# def show_post(request, post_slug):
#     one_post = get_object_or_404(Post, slug=post_slug)
#     comments = Comments_Post.objects.filter(post__slug=post_slug)
#     form = CommentForm(request.POST)
#
#     return render(request, 'blog/post.html', {'one_post': one_post, 'comments':comments, 'form':form})


class ShowCategory(PostMixin, ListView):
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


class SearchPosts(PostMixin,ListView):
    template_name = 'blog/search.html'

    context_object_name = 'posts'

    def get_queryset(self):
        q = self.request.GET.get('q')
        words = "".join(q[0].upper()) + q[1:]
        return Post.objects.filter(title__icontains = words, is_published=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context['title'] = 'Поиск Постов'
        return context

    # def get(self, request, *args, **kwargs):
    #     context = {}
    #
    #     question = request.GET.get('q')
    #     if question is not None:
    #         search_articles = Post.objects.filter(title__icontains = question)
    #
    #         # формируем строку URL, которая будет содержать последний запрос
    #         # Это важно для корректной работы пагинации
    #         context['last_question'] = '?q=%s' % question
    #
    #         current_page = Paginator(search_articles, 10)
    #
    #         page = request.GET.get('page')
    #         try:
    #             context['article_lists'] = current_page.page(page)
    #         except PageNotAnInteger:
    #             context['article_lists'] = current_page.page(1)
    #         except EmptyPage:
    #             context['article_lists'] = current_page.page(current_page.num_pages)
    #
    #             return render(template_name = self.template_name, context = context)