from applications.posts.views import PostByFollowedUsers
from django.urls import path

urlpatterns = [
    path('', PostByFollowedUsers.as_view(), name='ver posts'),
    
    
]