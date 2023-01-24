from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView

from users.forms import ProfileChangeForm, CustomUserCreationForm
from users.models import CustomUser


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class AccauntUser(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
        model = CustomUser
        form_class = ProfileChangeForm
        template_name = 'registration/profile_change.html'


        slug_url_kwarg = 'user_slug'


        def get_object(self, queryset=None):
            return self.request.user

        def get_success_url(self, **kwargs):
            return reverse_lazy('profile', kwargs={'user_slug': self.get_object().slug})
def profile(request, user_slug):
    profil = get_object_or_404(CustomUser, slug=user_slug)

    if request.user.is_authenticated != True:
        raise Http404()

    if profil.slug != request.user.slug:
        raise Http404()

    return render(request, 'users/profile.html', {'profil': profil})



