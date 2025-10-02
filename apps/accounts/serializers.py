from django.contrib.auth import authenticate
from rest_framework import serializers


from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Username yoki parol noto‘g‘ri.")
        else:
            raise serializers.ValidationError("Ikkala maydon ham to‘ldirilishi kerak.")

