from django.urls import path

from entries.views import (
    EntriesCreateView,
    EntriesDeleteView,
    EntriesDetailView,
    EntriesListView,
    EntriesUpdateView,
    HomeView,
)

app_name = "entries"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("entries/", EntriesListView.as_view(), name="entries_list"),
    path("<int:pk>/", EntriesDetailView.as_view(), name="entries_detail"),
    path("new/", EntriesCreateView.as_view(), name="entries_create"),
    path("<int:pk>/edit/", EntriesUpdateView.as_view(), name="entries_edit"),
    path("<int:pk>/delete/", EntriesDeleteView.as_view(), name="entries_delete"),
]
