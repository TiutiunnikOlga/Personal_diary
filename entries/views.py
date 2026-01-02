from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from entries.models import Entries


class EntriesViewSet(ModelViewSet):
    queryset = Entries.objects.all()
    serializer_class = EntriesSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        entries = serializer.save()
        entries.owner = self.request.user
        entries.save()

    def get_serializer_context(self):
        return {'request': self.request}
