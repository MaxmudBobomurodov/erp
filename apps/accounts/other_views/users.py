from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer, StudentSerializer
from apps.courses.models import Student


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None

class StudentCreateAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TeacherCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(role='teacher')
