from django.urls import reverse_lazy
from django.views.generic import CreateView

from blog.views import menu
from users.forms import CustomUserCreationForm

menu = [{'title': "Блог", 'url_name': 'blog'},
{'title': "Статьи", 'url_name': 'home'},
{'title': "Альбомы", 'url_name': 'home'},
{'title': "Платное", 'url_name': 'home'},
{'title': "О сайте", 'url_name': 'home'},
]


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/reg.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
