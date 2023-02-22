from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from albums.forms import CommentAlbumForm
from albums.models import Album, Votes_Album, Images
from albums.utils import AlbumsMixin



class AlbumList(AlbumsMixin, ListView):
    model = Album
    template_name = 'albums/albums.html'
    context_object_name = 'albums'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Альбомы'
        return context

    def get_queryset(self):
        return Album.objects.annotate(number_of_comments=Count('comments_album', filter=Q(comments_album__status=True))) \
            .filter(is_published=True) \
            .order_by('-title')

class ShowOrganSystem(AlbumsMixin, ListView):
    model = Album
    template_name = 'albums/organ_system.html'
    context_object_name = 'albums'
    allow_empty = False
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Система органов - ' + str(context['albums'][0].organ_system)
        context['organ_selected'] = context['albums'][0].organ_system.slug
        return context
    def get_queryset(self):
        return Album.objects.filter(organ_system__slug=self.kwargs['organ_slug'], is_published=True)\
            .annotate(number_of_comments=Count('comments_album', filter=Q(comments_album__status=True))) \
            .filter(is_published=True) \
            .order_by('-title')

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
        self.object = form.save(commit=False)
        self.object.album = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пост - ' + str(context['album'])
        album = get_object_or_404(Album, slug=self.kwargs['album_slug'])
        def get_vote(self):
            votes = Votes_Album.objects.filter(user=self.request.user.id, album=album)
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

    def get_modereted_comments(self):
        queryset = self.object.comments_album.filter(status=True)
        paginator = Paginator(queryset, 6)
        page = self.request.GET.get('page')
        comments = paginator.get_page(page)
        return comments

    def get_images(self):
        queryset = self.object.albumimages.all()
        paginator = Paginator(queryset, 2)
        page = self.request.GET.get('page')
        images = paginator.get_page(page)
        return images

def thumbsalbum(request):
    if request.POST.get('action') == 'thumbs':
        id = int(request.POST.get('albumid'))
        button = request.POST.get('button')
        update = Album.objects.get(id=id)

        if update.thumbs.filter(id=request.user.id).exists():
            q = Votes_Album.objects.get(
                Q(album_id=id) & Q(user_id=request.user.id))
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

class SearchAlbums(AlbumsMixin,ListView):
    template_name = 'albums/search.html'

    context_object_name = 'albums'

    def get_queryset(self):
        q = self.request.GET.get('q')
        words = "".join(q[0].upper()) + q[1:]
        return Album.objects.filter(title__icontains = words, is_published=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context['title'] = 'Поиск Альбомов'
        return context

