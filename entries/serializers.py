from rest_framework.serializers import ModelSerializer

from entries.models import Entries


class EntriesSerializer(ModelSerializer):
    class Meta:
        model = Entries
        fields = [
            'heading',
            'content',
            'photo',
            'created_at',
        ]