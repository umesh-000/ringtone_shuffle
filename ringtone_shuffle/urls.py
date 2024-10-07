from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('shuffle.urls')),
    path('api/', include('shuffle.urls_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)