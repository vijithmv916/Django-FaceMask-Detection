from .models import User, Client
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class ExtraFieldSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = Client
        fields = (
            "user",
            "location",
            "authority"
        )

    def create(self, validated_data):

        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.set_password(user_data['password'])
        user.save()
        full_client, created = Client.objects.update_or_create(
            user=user, location=validated_data.pop("location")
        )
        return full_client
