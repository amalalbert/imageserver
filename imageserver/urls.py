from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gallery.views import get_photo_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/images/', get_photo_urls), # This is your endpoint
]

# This helper allows Django to serve image files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)