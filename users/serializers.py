from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email уже зарегистрирован.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get("phone", ""),
        )
        return user

    class Meta:
        model = User
        fields = ["id", "email", "phone", "password"]
