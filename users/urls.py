from django.contrib.auth.views import LoginView
from django.urls import path

from users import views
from users.views import RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("profile/", views.profile, name="profile"),
]
