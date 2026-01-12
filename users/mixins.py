from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse


class EmailConfirmedRequiredMixin(LoginRequiredMixin):
    """Проверяем подтверждение mail"""
    def dispatch(self, request, *args, **kwargs):
        """Проверяем авторизауию пользователя"""
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        """Проверяем подтверждение email пользователя"""
        if not request.user.is_email_confirmed:
            return redirect(reverse("users:login"))

        return super().dispatch(request, *args, **kwargs)
