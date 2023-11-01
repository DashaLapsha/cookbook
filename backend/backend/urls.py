from django.contrib import admin
from django.urls import path, include
from authn import urls as authn_urls
from recipes import urls as recipes_urls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(authn_urls)),
    path('', include(recipes_urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)