from applications.posts.views import PostList, UserPostsList,PostByFollowedUsers
from django.urls import path

urlpatterns = [
    path('', PostList.as_view(), name='postear'),
    path('by_user/<pk>/', UserPostsList.as_view(), name='ver posts'),
    path('by_follows/', PostByFollowedUsers.as_view(), name='ver posts'),
    
    
]