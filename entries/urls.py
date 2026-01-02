from django.urls import path, include
from rest_framework.routers import DefaultRouter

from entries.apps import EntriesConfig
from entries.views import EntriesViewSet

app_name = EntriesConfig.name
router = DefaultRouter()
router.register(r'entries', EntriesViewSet)

urlpatterns = [
    path('entries/',include(router.urls) ),
]