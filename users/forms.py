from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    phone = forms.CharField(
        max_length=35,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Телефон"}
        ),
    )

    class Meta:
        model = User
        fields = ("email", "phone", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Эл. адрес", widget=forms.EmailInput(attrs={"autofocus": True})
    )

    def clean_username(self):
        email = self.cleaned_data.get("username")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email не найден.")
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "phone", "avatar"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.FileInput(attrs={"class": "form-control-file"}),
        }
        labels = {
            "email": "Email",
            "phone": "Телефон",
            "avatar": "Аватар",
        }
