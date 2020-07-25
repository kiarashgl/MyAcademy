"""MyAcademy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from . import settings

urlpatterns = [
	path('', include('core.urls')),
	path('accounts/', include('accounts.urls')),
	path('entities/', include('entities.urls')),
	path('ratings/', include('ratings.urls')),
	path('admin/', admin.site.urls),
	path('api-auth/', include('rest_framework.urls')),

	# Wagtail and Blog stuff
	path('cms-admin/', include(wagtailadmin_urls)),
	path('blog/', include(wagtail_urls)),
]

if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
