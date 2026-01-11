from django.contrib import admin

from entries.models import Entries


@admin.register(Entries)
class UsrAdmin(admin.ModelAdmin):
    list_filter = ("created_at",)
