from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('surveys.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('openapi', get_schema_view(
        title="Surveys API",
        description="Small API with surveys and questions",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui')
]
