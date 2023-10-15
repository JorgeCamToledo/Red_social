from applications.posts.views import PostList, UserPostsList
from django.urls import path

urlpatterns = [
    path('', PostList.as_view(), name='postear'),
    path('by_user/<pk>/', UserPostsList.as_view(), name='ver posts'),
    
    
]