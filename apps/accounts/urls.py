from django.urls import path

from apps.accounts.views import LoginAPIView, LogoutAPIView, MyView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('me/',MyView.as_view(), name='me'),
]