from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from entries.models import Entries


class EntriesSerializer(ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Entries
        fields = [
            "id",
            "heading",
            "content",
            "photo",
            "photo_url",
            "created_at",
        ]
        read_only_fields = ["created_at", "user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
