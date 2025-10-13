from django.contrib.auth import authenticate
from apps.accounts.models import User
from apps.courses.models import Student
from rest_framework import serializers
from django.core.mail import send_mail
import random

from apps.courses.models import Teacher


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']


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
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'full_name', 'email', 'phone', 'organization', 'is_activate', 'descriptions']

    def create(self, validated_data):
        full_name = validated_data.get('full_name')
        email = validated_data.get('email')
        phone = validated_data.get('phone')

        # ⚙️ Parol yaratish
        password = str(random.randint(100000, 999999))

        # ⚙️ User yaratish
        username = full_name.replace(" ", "_").lower()

        user = User.objects.create_user(
            username=username,
            email=email,
            role="student"
        )
        user.set_password(password)
        user.save()

        # ⚙️ Student yaratish
        student = Student.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            phone=phone,
            organization=validated_data.get('organization'),
            is_activate=validated_data.get('is_activate', False),
            descriptions=validated_data.get('descriptions', "")
        )

        # ⚙️ Parolni emailga yuborish
        try:
            send_mail(
                subject="Your Student Account Credentials",
                message=(
                    f"Hello {student.full_name}!\n\n"
                    f"Your username: {username}\n"
                    f"Your password: {password}\n\n"
                    "Please log in and change your password."
                ),
                from_email="maxmudbobomurodov151@gmail.com",
                recipient_list=[student.email],
                fail_silently=True,  # Email xato bo‘lsa, serializer ishlashni to‘xtatmaydi
            )
        except Exception as e:
            print(f"Email error: {e}")

        return student

class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Teacher
        fields = ['id','user', 'full_name', 'email', 'phone', 'descriptions']

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

class SuperuserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}