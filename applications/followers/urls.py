from django.urls import path
from applications.followers.views import FollowView 

urlpatterns = [
    path('follow/', FollowView.as_view(), name='follow'),
]