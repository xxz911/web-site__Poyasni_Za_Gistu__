from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/reg.html'
    success_url = reverse_lazy('login')

