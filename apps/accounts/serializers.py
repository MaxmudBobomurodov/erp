from django.contrib.auth import authenticate
from rest_framework import serializers


from apps.accounts.models import User
from apps.courses.models import Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','role']

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

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop("user", None)  # ⚡️ user bo‘lmasa None bo‘lsin
        if user_data:
            user = User.objects.create(**user_data, role="student")
        else:
            user = User.objects.create_user(
                username=validated_data["full_name"].replace(" ", "").lower(),
                password="12345678",
                role="student"
            )
        student = Student.objects.create(user=user, **validated_data)
        return student