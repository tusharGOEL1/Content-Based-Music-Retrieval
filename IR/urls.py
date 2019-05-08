"""IR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from project import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r"^$", views.music_retrieval),
    url(r"^$", views.music_retrieval),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, serve, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)
