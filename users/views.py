from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import (EmailAuthenticationForm, RegistrationForm,
                         UserProfileForm)
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("entries:entries_list")

    def form_valid(self, form):
        user = form.save(commit=True)
        login(self.request, user)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context


@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect("profile")
        else:
            messages.error(request, "Проверьте ошибки в форме.")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form, "user": user})


class CustomLoginView(LoginView):
    form_class = EmailAuthenticationForm
    template_name = "accounts/login.html"
    success_url = "/"
