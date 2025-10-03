from django.urls import path

from apps.accounts.other_views.users import UserListAPIView, StudentCreateAPIView
from apps.accounts.views import LoginAPIView, LogoutAPIView, MyView

app_name = "accounts"

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/me/',MyView.as_view(), name='me'),
    path('users/',UserListAPIView.as_view(), name='users'),
    path('users/create/student/', StudentCreateAPIView.as_view(), name='student-create'),
]