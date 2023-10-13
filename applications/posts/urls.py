from applications.posts.views import PostList 
from django.urls import path

urlpatterns = [
    path('', PostList.as_view(), name='postear'),
    
]