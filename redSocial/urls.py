from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('applications.authentication.urls')),
    path('api/v1/post/', include('applications.posts.urls')),
    path('api/v1/profile/', include('applications.profiles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
