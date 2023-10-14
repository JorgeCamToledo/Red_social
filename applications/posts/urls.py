from applications.posts.views import PostList, UserPostsList
from django.urls import path

urlpatterns = [
    path('', PostList.as_view(), name='postear'),
    path('<pk>/', UserPostsList.as_view(), name='ver posts'),
    
    
]