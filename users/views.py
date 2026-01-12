import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import EmailAuthenticationForm, RegistrationForm, UserProfileForm
from users.models import User

logger = logging.getLogger(__name__)


class RegisterView(CreateView):
    """Представдение для нового пользователя"""
    model = User
    form_class = RegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("entries:entries_list")

    def form_valid(self, form):
        """Обработка формы регистрации"""
        user = form.save(commit=False)
        user.username = user.email
        user.is_email_confirmed = False
        user.save()

        """Отправка письма подтверждения на почту"""
        send_confirmation_email(self.request, user)

        messages.success(
            self.request,
            "Регистрация успешна! Проверьте почту для подтверждения email.",
        )
        login(self.request, user)
        return redirect(self.success_url)


@login_required
def profile(request):
    """Редакирование профиля пользователя"""
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect("users:profile")
        else:
            messages.error(request, "Проверьте ошибки в форме.")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form, "user": user})


class CustomLoginView(LoginView):
    """Представление для авторизации пользователя"""
    form_class = EmailAuthenticationForm
    template_name = "accounts/login.html"
    success_url = "/"


def send_confirmation_email(request, user):
    """Формирование письма подтверждения новому пользователю"""
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = user.email_confirmation_token
    confirmation_url = reverse(
        "users:confirm_email", kwargs={"uidb64": uid, "token": str(token)}
    )
    confirmation_link = f"http://{domain}{confirmation_url}"

    subject = "Подтвердите ваш email"
    message = f"""
    Здравствуйте!

    Для подтверждения email перейдите по ссылке:
    {confirmation_link}

    Если вы не регистрировались на сайте, проигнорируйте это письмо.
    """

    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


class EmailVerificationView(View):
    """Обработка подтверждения email"""
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and str(user.email_confirmation_token) == token:
            user.is_email_confirmed = True
            user.save()
            messages.success(
                request, "Email подтверждён! Теперь можно пользоваться всеми функциями."
            )
            return redirect("entries:entries_list")
        else:
            return HttpResponse("Ссылка недействительна или уже использована.")
