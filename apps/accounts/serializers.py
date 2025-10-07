from django.contrib.auth import authenticate
from apps.accounts.models import User
from apps.courses.models import Student
from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random

from apps.courses.models import Teacher




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
        fields = ['user','full_name', 'email', 'phone','role']

    def create(self, validated_data):
        password = str(random.randint(100000,999999))

        user = User.objects.create_user(
            username=validated_data['full_name'],
            email=validated_data['email'],
        )
        user.set_password(password)
        user.save()

        student = Student.objects.create(
            user=user,
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            role="student"
        )

        send_mail(
            subject="Your student Account Password",
            message=f"Hello {student.full_name}!,,your username{student.full_name} your student account password is {password}",
            from_email="maxmudbobomurodov151@gmail.com",
            recipient_list=[student.email],
            fail_silently=False,
        )
        return student


class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Teacher
        fields = ['user', 'full_name', 'email', 'phone', 'descriptions']

    def create(self, validated_data):
        password = str(random.randint(100000, 999999))

        user = User.objects.create_user(
            username=validated_data['full_name'],
            email=validated_data['email'],
            role="teacher"
        )
        user.set_password(password)
        user.save()

        # Teacher yaratish
        teacher = Teacher.objects.create(
            user=user,
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            descriptions=validated_data.get('descriptions', ''),
        )

        # Parolni email orqali yuborish
        send_mail(
            subject="Your Teacher Account Password",
            message=(
                f"Hello {teacher.full_name}!\n\n"
                f"Your username: {teacher.full_name}\n"
                f"Your password: {password}\n\n"
                "Please change your password after first login."
            ),
            from_email="maxmudbobomurodov151@gmail.com",
            recipient_list=[teacher.email],
            fail_silently=False,
        )
        print('*********************************************')

        return teacher
