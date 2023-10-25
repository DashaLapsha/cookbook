from django.contrib import admin
from django.urls import path, include
from authn import urls as authn_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(authn_urls)),
]