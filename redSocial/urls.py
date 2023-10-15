from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('applications.authentication.urls')),
    path('api/v1/post/', include('applications.posts.urls')),
    path('api/v1/profile/', include('applications.profiles.urls')),
    path('api/v1/follower/', include('applications.followers.urls')),
    path('api/v1/follow_request/', include('applications.follow_request.urls')),
    path('api/v1/comment/', include('applications.comments.urls')),
    path('api/v1/home/', include('applications.posts.urls_home')),
    path('api/v1/reaction/', include('applications.reactions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
