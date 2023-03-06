from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from articles.forms import CommentArticleForm
from articles.models import Article, Votes_Article, Thematic
from articles.utils import ArticleMixin


# Класс представления для списка Статей
class ArticlesList(ArticleMixin, ListView):
    model = Article
    template_name = 'articles/articles.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        return context

    def get_queryset(self):
        # Выборка всех статей которые опубликованы + их комментарии, которые прошли проверку модератором
        return Article.objects.annotate(number_of_comments=Count('comments_article', filter=Q(comments_article__status=True)))\
            .filter(is_published=True)\
            .order_by('-time_create').select_related('thematic')


# Класс представления для списка статей по тематикам
class ShowThematic(ArticleMixin, ListView):
    model = Article
    template_name = 'articles/thematic.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        t = Thematic.objects.get(slug=self.kwargs['thematic_slug'])
        context['title'] = 'Тематика - ' + str(t.name)
        context['thematic_selected'] = t.slug
        return context

    def get_queryset(self):
        # Выборка всех опубликованных статей по тематикам + их комментарии, которые прошли проверку модератором
        return Article.objects.filter(thematic__slug=self.kwargs['thematic_slug'], is_published=True)\
            .annotate(number_of_comments=Count('comments_article', filter=Q(comments_article__status=True))) \
            .filter(is_published=True) \
            .order_by('-title').select_related('thematic')


# Класс представления для конкретной Статьи
class ArticleDetail(SuccessMessageMixin, FormMixin, DetailView):
    model = Article
    template_name = 'articles/article.html'
    context_object_name = 'article'
    slug_url_kwarg = 'article_slug'
    form_class = CommentArticleForm
    success_message = 'Комментарий успешно отправлен! Ожидайте проверку модератором!'

    def get_success_url(self, **kwargs):
        return reverse_lazy('article', kwargs={'article_slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # При валидной форме комментария заполняем данные о статье и авторе и сохраняем
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        context['title'] = 'Статья - ' + str(obj.title)

        # Метод для проверки голоса для авторизированного пользователя
        def get_vote(self):
            votes = Votes_Article.objects.filter(user=self.request.user.id, article=obj)
            if len(votes) == 0:
                return 'not_vote'
            if len(votes) == 1:
                if votes[0].vote == 0:
                    return 'down'
                if votes[0].vote == 1:
                    return "up"
            else:
                raise TypeError('Ошибка в VoteArticle')
        context['vote_article'] = get_vote(self)
        comments = self.get_modereted_comments()
        context['comments'] = comments
        context['page_obj'] = comments

        return context

    # Метод для пагинации комментариев
    def get_modereted_comments(self):
        queryset = self.object.comments_article.filter(status=True).select_related('author')
        paginator = Paginator(queryset, 6)
        page = self.request.GET.get('page')
        comments = paginator.get_page(page)
        return comments


# Метод обработки голосования
def thumbsarticle(request):
    if request.POST.get('action') == 'thumbs':
        # Получаем данные из запроса Ajax
        id = int(request.POST.get('articleid'))
        button = request.POST.get('button')
        update = Article.objects.get(id=id)

        # Проверяем голосовал ли пользователь
        if update.thumbs.filter(id=request.user.id).exists():
            q = Votes_Article.objects.get(
                Q(article_id=id) & Q(user_id=request.user.id))
            evote = q.vote

            # Ниже прибавляем/убираем его голос из таблицы Article и обновляем запись в таблице Votes_Article
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

                new = Votes_Article(article_id=id, user_id=request.user.id, vote=True)
                new.save()
            else:

                update.thumbsdown = F('thumbsdown') + 1
                update.thumbs.add(request.user)
                update.save()

                new = Votes_Article(article_id=id, user_id=request.user.id, vote=False)
                new.save()

            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown

            return JsonResponse({'up': up, 'down': down})

    pass

# Класс представления для поиска Статьи
class SearchArticles(ArticleMixin,ListView):
    template_name = 'articles/search.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Получаем данные из запроса поиска
        q = self.request.GET.get('q')
        words = "".join(q[0].upper()) + q[1:]
        # Делаем выборку из опубликованных статей на совпадение по заголовку
        # (На SQLite работает не коректно, на основных реляционных СУБД работает коректно)
        return Article.objects.filter(title__icontains = words, is_published=True).annotate(number_of_comments=Count('comments_article', filter=Q(comments_article__status=True))).select_related('thematic')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context['title'] = f'Поиск Статей: ' + self.request.GET.get('q')
        return context

