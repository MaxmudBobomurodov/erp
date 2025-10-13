import random
from os import access

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer, LoginSerializer
from config import settings


class LoginAPIView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'detail:invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class MyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ChangeUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        user = request.user

        if not old_password or not new_password:
            return Response({'error': 'Both old_password and new_password are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) != 6:
            return Response({'error': 'New password must be exactly 6 digits.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not new_password.isdigit():
            return Response({'error': 'New password must contain digits only.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password changed successfully.'},
                        status=status.HTTP_200_OK)


class ResetUserPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = str(random.randint(100000, 999999))
        cache.set(email, otp, timeout=300)
        send_mail(
            subject='Password Reset otp',
            message=f'your otp password is {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return Response({'detail': 'Otp sent successfully to your email.'},
                        status=status.HTTP_200_OK,)

class VerifyOtpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        saved_otp = cache.get(email)
        if saved_otp is None:
            return Response({'error': 'Invalid Otp.'}, status=status.HTTP_404_NOT_FOUND)

        if otp != saved_otp:
            return Response({'error': 'Otp does not match.'}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(email)
        token = RefreshToken.for_user(User.objects.get(email=email))
        return Response({'detail': 'Otp verified successfully.', 'token': str(token.access_token)},status=status.HTTP_200_OK)

class SetNewPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            return Response({'error': 'Old password and new password are not the same.'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        user.set_password(password)
        user.save()
        print(user, password)
        return Response({'detail': 'Password changed successfully.'},status=status.HTTP_200_OK)