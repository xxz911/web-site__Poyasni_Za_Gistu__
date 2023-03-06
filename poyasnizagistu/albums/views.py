from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from albums.forms import CommentAlbumForm
from albums.models import Album, Votes_Album, Organ_System
from albums.utils import AlbumsMixin


# Класс представления для списка Альбомов
class AlbumList(AlbumsMixin, ListView):
    model = Album
    template_name = 'albums/albums.html'
    context_object_name = 'albums'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Альбомы'
        return context

    def get_queryset(self):
        # Выборка всех альбомов которые опубликованы + их комментарии, которые прошли проверку модератором
        return Album.objects.annotate(number_of_comments=Count('comments_album', filter=Q(comments_album__status=True))) \
            .filter(is_published=True) \
            .order_by('-title').select_related('organ_system')


# Класс представления для списка альбомов по системам органов
class ShowOrganSystem(AlbumsMixin, ListView):
    model = Album
    template_name = 'albums/organ_system.html'
    context_object_name = 'albums'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        o = Organ_System.objects.get(slug=self.kwargs['organ_slug'])
        context['title'] = 'Система органов - ' + str(o.name)
        context['organ_selected'] = o.slug
        return context

    def get_queryset(self):
        # Выборка всех опубликованных альбомов по системам органов + их комментарии, которые прошли проверку модератором
        return Album.objects.filter(organ_system__slug=self.kwargs['organ_slug'], is_published=True)\
            .annotate(number_of_comments=Count('comments_album', filter=Q(comments_album__status=True))) \
            .filter(is_published=True) \
            .order_by('-title').select_related('organ_system')


# Класс представления для конкретного Альбома
class AlbumDetail(SuccessMessageMixin, FormMixin, DetailView):
    model = Album
    template_name = 'albums/album.html'
    context_object_name = 'album'
    slug_url_kwarg = 'album_slug'
    form_class = CommentAlbumForm
    success_message = 'Комментарий успешно отправлен! Ожидайте проверку модератором!'

    def get_success_url(self, **kwargs):
        return reverse_lazy('album', kwargs={'album_slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # При валидной форме комментария заполняем данные о альбоме и авторе и сохраняем
        self.object = form.save(commit=False)
        self.object.album = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        context['title'] = 'Альбом - ' + str(obj.title)

        # Метод для проверки голоса для авторизированного пользователя
        def get_vote(self):
            votes = Votes_Album.objects.filter(user=self.request.user.id, album=obj)
            if len(votes) == 0:
                return 'not_vote'
            if len(votes) == 1:
                if votes[0].vote == 0:
                    return 'down'
                if votes[0].vote == 1:
                    return "up"
            else:
                raise TypeError('Ошибка в VoteAlbums')
        context['vote_album'] = get_vote(self)
        comments = self.get_modereted_comments()
        images = self.get_images()
        context['images'] = images
        context['page_obj_img'] = images
        context['comments'] = comments
        context['page_obj'] = comments

        return context

    # Метод для пагинации комментариев
    def get_modereted_comments(self):
        queryset = self.object.comments_album.filter(status=True).select_related('author')
        paginator = Paginator(queryset, 6)
        page = self.request.GET.get('page')
        comments = paginator.get_page(page)
        return comments

    # Метод для пагинации изображений в альбоме
    def get_images(self):
        queryset = self.object.albumimages.all()
        paginator = Paginator(queryset, 2)
        page = self.request.GET.get('page')
        images = paginator.get_page(page)
        return images


# Метод обработки голосования
def thumbsalbum(request):
    if request.POST.get('action') == 'thumbs':
        # Получаем данные из запроса Ajax
        id = int(request.POST.get('albumid'))
        button = request.POST.get('button')
        update = Album.objects.get(id=id)

        # Проверяем голосовал ли пользователь
        if update.thumbs.filter(id=request.user.id).exists():
            q = Votes_Album.objects.get(
                Q(album_id=id) & Q(user_id=request.user.id))
            evote = q.vote

            # Ниже прибавляем/убираем его голос из таблицы Album и обновляем запись в таблице Votes_Album
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

                new = Votes_Album(album_id=id, user_id=request.user.id, vote=True)
                new.save()
            else:

                update.thumbsdown = F('thumbsdown') + 1
                update.thumbs.add(request.user)
                update.save()

                new = Votes_Album(album_id=id, user_id=request.user.id, vote=False)
                new.save()

            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown

            return JsonResponse({'up': up, 'down': down})

    pass


# Класс представления для поиска Альбома
class SearchAlbums(AlbumsMixin,ListView):
    template_name = 'albums/search.html'
    context_object_name = 'albums'

    def get_queryset(self):
        # Получаем данные из запроса поиска
        q = self.request.GET.get('q')
        words = "".join(q[0].upper()) + q[1:]
        # Делаем выборку из опубликованных альбомов на совпадение по заголовку
        # (На SQLite работает не коректно, на основных реляционных СУБД работает коректно)
        return Album.objects.filter(title__icontains = words, is_published=True).annotate(number_of_comments=Count('comments_album', filter=Q(comments_album__status=True))).select_related('organ_system')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context['title'] = f'Поиск Альбомов: ' + self.request.GET.get('q')
        return context
