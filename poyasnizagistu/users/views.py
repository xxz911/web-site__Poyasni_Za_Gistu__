from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
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


class AccauntUser(LoginRequiredMixin, UpdateView):
        model = CustomUser
        form_class = ProfileChangeForm
        template_name = 'registration/profile_change.html'
        success_url = reverse_lazy('profile')

        def get_object(self, queryset=None):
            return self.request.user


def profile(request):
    profil = CustomUser.objects.all()


    return render(request, 'users/profile.html')



