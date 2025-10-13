"""
URL configuration for config project.

The `urlpatterns` list routes URLs to other_views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function other_views
    1. Add an import:  from my_app import other_views
    2. Add a URL to urlpatterns:  path('', other_views.home, name='home')
Class-based other_views
    1. Add an import:  from other_app.other_views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view  # ✅ to‘g‘ri import shu
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="ERP System API",
        default_version='v1',
        description="ERP tizimi uchun auto-generated API hujjatlar",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="support@erp-system.uz"),
        license=openapi.License(name="Proprietary License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ]
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/', include(
      [
         path('', include('apps.accounts.urls')),
         path('attendance/', include('apps.attendances.urls')),
         path('courses/', include('apps.courses.urls')),

      ]
   )),

   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]