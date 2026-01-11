from django import forms

from .models import Entries


class EntriesForm(forms.ModelForm):
    class Meta:
        model = Entries
        fields = ["heading", "content", "photo"]
        widgets = {
            "heading": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите заголовок"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Напишите что-нибудь...",
                }
            ),
        }
        labels = {
            "heading": "Заголовок",
            "content": "Содержимое",
            "photo": "Фото",
        }
        help_texts = {
            "heading": "Краткий заголовок вашей записи",
            "content": "Основной текст дневника",
            "photo": "При желании добавьте изображение",
        }

    def clean_heading(self):
        """
        Валидация заголовка (пример).
        """
        heading = self.cleaned_data.get("heading")
        if len(heading) < 3:
            raise forms.ValidationError("Заголовок должен быть не короче 3 символов.")
        return heading
