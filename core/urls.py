"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# django imports occur at runtime, so fail linter
# pylint:disable=import-error
from django.contrib import admin
from django.urls import path, include
# pylint:enable=import-error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webapp.urls'), name='webapp_urls'),
    path("accounts/", include("allauth.urls")),
]

# Pylint assumes incorrect gloabal var
# pylint:disable=invalid-name
handler404 = 'webapp.views.error_404'
handler403 = 'webapp.views.error_403'
handler500 = 'webapp.views.error_500'
# pylint:enable=invalid-name
