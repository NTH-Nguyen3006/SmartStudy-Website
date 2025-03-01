"""
URL configuration for SmartStudy_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi, views
from django.conf import settings
from django.conf.urls.static import static

schemas_view = views.get_schema_view(
    openapi.Info(
        title='SmartStudy API',
        default_version='v1',
        description='API for get Data',
        license=openapi.License(name="SSBOT")
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SSApp.urls')),
    # path('social-auth', include('social_django.urls', namespace='social')), 

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
            schemas_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schemas_view.with_ui(cache_timeout=0),
            name='schema-ui'),
    re_path(r'^redoc/$', schemas_view.with_ui('redoc', cache_timeout=0), 
            name='schema-redoc')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
