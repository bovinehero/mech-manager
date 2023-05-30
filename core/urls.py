from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403, handler404, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webapp.urls'), name='webapp_urls'),
    path("accounts/", include("allauth.urls")),
]

handler404 = 'webapp.views.error_404'
handler403 = 'webapp.views.error_403'
handler500 = 'webapp.views.error_500'
